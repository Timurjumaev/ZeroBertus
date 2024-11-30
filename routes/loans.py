from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.loans import create_loan_f
from routes.login import get_current_active_user
from schemas.users import CreateUser
from schemas.loans import CreateLoan
from db import database


loans_router = APIRouter(
    prefix="/loans",
    tags=["Loans operation"]
)


@loans_router.post('/create')
def create_worker(form: CreateLoan, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    create_loan_f(form=form, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")




