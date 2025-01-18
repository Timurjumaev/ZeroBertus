from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.incomes import get_incomes, create_income_f, delete_income_f
from schemas.incomes import CreateIncome, Type
from datetime import date
from routes.login import get_current_active_user
from schemas.users import CreateUser
from db import database


incomes_router = APIRouter(
    prefix="/incomes",
    tags=["Incomes Operation"]
)


@incomes_router.get('/get')
def get(ident: int = 0, search: str = None, _type: Type = None, start_date: date = None,
        end_date: date = None, page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    return get_incomes(ident, search, _type, start_date, end_date, page, limit, db)


@incomes_router.post('/create')
def create_income(form: CreateIncome, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    create_income_f(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@incomes_router.delete('/delete')
def delete_income(ident: int, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    delete_income_f(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
