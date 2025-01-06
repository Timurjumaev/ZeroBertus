from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.salaries import create_salary_f, get_salaries_f, delete_salary_f
from datetime import date
from routes.login import get_current_active_user
from schemas.users import CreateUser
from schemas.salaries import CreateSalary, Type
from db import database


salaries_router = APIRouter(
    prefix="/salaries",
    tags=["Salaries operation"]
)


@salaries_router.get('/get')
def get(ident: int = 0, _type: Type = None,  start_date: date = None,
        end_date: date = None, page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    return get_salaries_f(ident, _type, start_date, end_date, page, limit, db)


@salaries_router.post('/create')
def create_worker(form: CreateSalary, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    create_salary_f(form=form, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@salaries_router.delete('/delete')
def delete_salary(ident: int, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    delete_salary_f(ident, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")




