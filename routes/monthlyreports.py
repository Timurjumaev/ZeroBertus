from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.monthlyreports import get_monthly_reports, confirmation_monthly_report_f
from datetime import date
from routes.login import get_current_active_user
from schemas.users import CreateUser
from db import database


monthly_reports_router = APIRouter(
    prefix="/monthly_reports",
    tags=["Monthly Reports Operation"]
)


@monthly_reports_router.get('/get')
def get(ident: int = 0, status: bool = None, start_date: date = None,
        end_date: date = None, page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    return get_monthly_reports(ident, status, start_date, end_date, page, limit, db)


@monthly_reports_router.put("/confirmation")
def confirmation_monthly_report(db: Session = Depends(database),
                                current_user: CreateUser = Depends(get_current_active_user)):
    confirmation_monthly_report_f(db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
