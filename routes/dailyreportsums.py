from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.dailyreportsums import (get_daily_report_sums, create_daily_report_sum_f,
                                       refresh_daily_report_sum_f, confirmation_daily_report_sum_f)
from datetime import date
from routes.login import get_current_active_user
from schemas.users import CreateUser
from db import database


daily_report_sums_router = APIRouter(
    prefix="/daily_report_sums",
    tags=["Daily Sums Reports Operation"]
)


@daily_report_sums_router.get('/get')
def get(ident: int = 0, status: bool = None, start_date: date = None,
        end_date: date = None, page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    return get_daily_report_sums(ident, status, start_date, end_date, page, limit, db)


@daily_report_sums_router.post('/create')
def create_daily_report_sum(db: Session = Depends(database),
                            current_user: CreateUser = Depends(get_current_active_user)):
    create_daily_report_sum_f(db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@daily_report_sums_router.put("/update")
def refresh_daily_report_sum(db: Session = Depends(database),
                             current_user: CreateUser = Depends(get_current_active_user)):
    refresh_daily_report_sum_f(db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@daily_report_sums_router.put("/confirmation")
def confirmation_daily_report_sum(db: Session = Depends(database),
                                  current_user: CreateUser = Depends(get_current_active_user)):
    confirmation_daily_report_sum_f(db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")



