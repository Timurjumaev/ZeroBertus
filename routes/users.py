from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.users import get_user, create_user_f, update_user_own
from routes.login import get_current_active_user
from schemas.users import CreateUser, UpdateUser
from db import database


users_router = APIRouter(
    prefix="/users",
    tags=["Users operation"]
)


@users_router.get('/get')
def get(current_user: CreateUser = Depends(get_current_active_user)):
    return get_user(usr=current_user)


@users_router.post('/create')
def create_user(form: CreateUser, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    create_user_f(form=form, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@users_router.put("/update_own")
def update_user(form: UpdateUser, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_active_user)):
    update_user_own(usr=current_user, form=form, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")



