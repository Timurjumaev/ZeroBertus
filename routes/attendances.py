from fastapi import UploadFile, File, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from db import database
from datetime import datetime
import pandas as pd
from io import BytesIO
from models.workers import Workers
from models.attendances import Attendances
from routes.login import get_current_active_user
from schemas.users import CreateUser

attendances_router = APIRouter(
    prefix="/attendances",
    tags=["Attendances operation"]
)


@attendances_router.post("/import-attendance/")
async def import_attendance(file: UploadFile = File(...), db: Session = Depends(database),
                            current_user: CreateUser = Depends(get_current_active_user)):
    # Faqat Excel fayllariga ruxsat beramiz
    if file.content_type not in ["application/vnd.ms-excel",  # .xls
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:  # .xlsx
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel (.xls or .xlsx) file.")

    # Faylni o'qish
    contents = await file.read()
    try:
        # Fayl formatini aniqlash
        if file.content_type == "application/vnd.ms-excel":  # .xls
            # Faylni pandas yordamida yuklab, .xlsx formatga o‘tkazib ishlatish
            xls_file = pd.ExcelFile(BytesIO(contents), engine="xlrd")
            data = xls_file.parse(sheet_name=0)  # 1-varaqqa murojaat
        else:  # .xlsx
            data = pd.read_excel(BytesIO(contents), engine='openpyxl')  # .xlsx format
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the file: {str(e)}")

    # Faqat kerakli qatorlardan boshlab o'qish
    data = data.iloc[4:]  # 5-qatordan boshlab, haqiqiy ma'lumotlarni olish

    # Sarlavha ustunlarini qo'lda belgilash
    data.columns = [
        'index', 'person_id', 'name', 'department', 'position', 'gender', 'date', 'day_of_week',
        'schedule', 'check_in', 'check_out', 'work_time', 'overtime', 'attendance', 'lateness',
        'early_leave', 'absence', 'leave', 'status', 'records'
    ]

    # Yangi ustun nomlarini ko'rsatish uchun chop etish
    print(data.columns)
    print(data.head())

    # Qatorlarni qayta ishlash
    for index, row in data.iterrows():
        worker_name = row.get('name')

        # Mavjud xodimni izlash yoki xato qaytarish
        worker = db.query(Workers).filter(Workers.name == worker_name).first()
        if worker is None:
            raise HTTPException(status_code=400, detail=f"Kechirasiz, {worker_name} ismli ishchi topilmadi")

        # Excel qatorlarini qayta ishlash
        row_date = row['date']
        if isinstance(row_date, str):  # Sanani `datetime.date` ga aylantirish
            row_date = datetime.strptime(row_date, "%Y-%m-%d").date()

        # Kelgan va ketgan vaqtlarni o'zgartirish
        row_check_in = row['check_in']
        if isinstance(row_check_in, str):
            try:
                row_check_in = datetime.strptime(row_check_in, "%H:%M:%S").time()
            except ValueError:
                row_check_in = None  # Noto'g'ri vaqt bo'lsa, None

        row_check_out = row['check_out']
        if isinstance(row_check_out, str):
            try:
                row_check_out = datetime.strptime(row_check_out, "%H:%M:%S").time()
            except ValueError:
                row_check_out = None  # Noto'g'ri vaqt bo'lsa, None

        # `datetime.combine` uchun to'g'ri vaqtlarni birlashtirish yoki `None`ni saqlash
        came_datetime = None if row_check_in is None else datetime.combine(row_date, row_check_in)
        went_datetime = None if row_check_out is None else datetime.combine(row_date, row_check_out)

        if db.query(Attendances).filter(Attendances.worker_id == worker.id,
                                        Attendances.date == row_date).first():
            raise HTTPException(status_code=400, detail="Ushbu kun uchun davomat allaqachon saqlangan!")

        # Davomat yozuvini yaratish
        attendance = Attendances(
            date=row_date,
            came_datetime=came_datetime,
            went_datetime=went_datetime,
            worker_id=worker.id
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        money_for_one_day = worker.fixed / worker.workdays
        if attendance.came_datetime:
            db.query(Workers).filter(Workers.name == worker_name).update({
                Workers.balance: Workers.balance + money_for_one_day
            })
            db.commit()
    return {"status": "Attendance data imported successfully"}