from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.expenses import get_expenses, create_expense_f
from schemas.expenses import CreateExpense, Type
from datetime import date
from routes.login import get_current_active_user
from schemas.users import CreateUser
from db import database


expenses_router = APIRouter(
    prefix="/expenses",
    tags=["Expenses Operation"]
)


@expenses_router.get('/get')
def get(ident: int = 0, _type: Type = None,  start_date: date = None,
        end_date: date = None, page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    return get_expenses(ident, _type, start_date, end_date, page, limit, db)


@expenses_router.post('/create')
def create_expense(form: CreateExpense, db: Session = Depends(database),
                   current_user: CreateUser = Depends(get_current_active_user)):
    create_expense_f(form, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")