import math
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.workers import Workers
from models.attendances import Attendances
from utils.db_operations import save_in_db, get_in_db
from sqlalchemy import func
from datetime import datetime


def get_workers(ident, search, part, page, limit, db):
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    # Bugungi sanani olish
    current_year = datetime.now().year
    current_month = datetime.now().month

    if ident > 0:
        ident_filter = Workers.id == ident
    else:
        ident_filter = Workers.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Workers.name.like(search_formatted)
    else:
        search_filter = Workers.id > 0

    if part:
        part_filter = Workers.part == part
    else:
        part_filter = Workers.id > 0

    # Workerlarni olish va sanalar bo'yicha filtr
    items = db.query(Workers).options(
        joinedload(Workers.attendances),
        joinedload(Workers.loans),
        joinedload(Workers.salaries),
    ).filter(ident_filter, search_filter, part_filter).order_by(Workers.name)

    # Bugungi yil va oyda qancha davomat borligini hisoblash
    attendance_count = db.query(func.count(Attendances.id))\
        .join(Workers).filter(
            ident_filter, search_filter, part_filter,
            func.extract('year', Attendances.date) == current_year,
            func.extract('month', Attendances.date) == current_month
        ).scalar()

    if page and limit:
        return {"attendance_count": attendance_count, "current_page": page, "limit": limit, "pages": math.ceil(items.count() / limit),
                "data": items.offset((page - 1) * limit).limit(limit).all()}
    else:
        return {"data": items.all()}


def create_worker_f(form, db):
    if db.query(Workers).filter(Workers.name == form.name).first():
        raise HTTPException(status_code=400, detail="Bunday ismli ishchi avval ro'yxatga olingan!")
    new_item_db = Workers(
        name=form.name,
        workdays=form.workdays,
        fixed=form.fixed,
        part=form.part
    )
    save_in_db(db, new_item_db)


def update_worker_f(form, db):
    get_in_db(db, Workers, form.id)
    db.query(Workers).filter(Workers.id == form.id).update({
        Workers.name: form.name,
        Workers.workdays: form.workdays,
        Workers.fixed: form.fixed,
        Workers.part: form.part,
        Workers.balance: form.balance
    })
    db.commit()


def delete_worker_f(ident, db):
    get_in_db(db, Workers, ident)
    db.query(Workers).filter(Workers.id == ident).delete()
    db.commit()


