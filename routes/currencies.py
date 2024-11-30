from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.currencies import get_currencies, create_currency_f
from routes.login import get_current_active_user
from schemas.users import CreateUser
from schemas.currencies import CreateCurrency
from db import database


currencies_router = APIRouter(
    prefix="/currencies",
    tags=["Currencies operation"]
)


@currencies_router.get('/get')
def get(ident: int = 0, status: bool = None, page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    return get_currencies(ident, status, page, limit, db)


@currencies_router.post('/create')
def create_worker(form: CreateCurrency, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    create_currency_f(form=form, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")




