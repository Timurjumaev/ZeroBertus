from models.monthlyreports import MonthlyReports
from utils.db_operations import get_in_db
from utils.pagination import pagination
from fastapi import HTTPException


def get_monthly_reports(ident, status, start_date, end_date, page, limit, db):
    if ident > 0:
        ident_filter = MonthlyReports.id == ident
    else:
        ident_filter = MonthlyReports.id > 0

    if status is None:
        status_filter = MonthlyReports.id > 0
    elif status:
        status_filter = MonthlyReports.status == True
    else:
        status_filter = MonthlyReports.status == False

    if start_date:
        start_date_filter = MonthlyReports.date >= start_date
    else:
        start_date_filter = MonthlyReports.id > 0

    if end_date:
        end_date_filter = MonthlyReports.date <= end_date
    else:
        end_date_filter = MonthlyReports.id > 0

    items = (db.query(MonthlyReports).filter(ident_filter, status_filter, start_date_filter, end_date_filter)
             .order_by(MonthlyReports.id.desc()))

    return pagination(items, page, limit)


def confirmation_monthly_report_f(db):
    report = db.query(MonthlyReports).filter(MonthlyReports.status == True).first()
    if report is None:
        raise HTTPException(status_code=400, detail="Amaliyot allaqachon yakunlangan!")
    else:
        db.query(MonthlyReports).filter(MonthlyReports.status == True).update({
            MonthlyReports.status: False
        })
        db.commit()
