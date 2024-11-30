from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.workers import get_workers, create_worker_f, update_worker_f, delete_worker_f
from routes.login import get_current_active_user
from schemas.users import CreateUser
from schemas.workers import CreateWorker, UpdateWorker
from db import database
from schemas.workers import Part


workers_router = APIRouter(
    prefix="/workers",
    tags=["Workers operation"]
)


@workers_router.get('/get')
def get(ident: int = 0, search: str = None, part: Part = None, page: int = 1,
        limit: int = 25, db: Session = Depends(database),
        current_user: CreateUser = Depends(get_current_active_user)):
    return get_workers(ident, search, part, page, limit, db)


@workers_router.post('/create')
def create_worker(form: CreateWorker, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    create_worker_f(form=form, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@workers_router.put("/update")
def update_worker(form: UpdateWorker, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    update_worker_f(form=form, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@workers_router.delete("/delete")
def delete_worker(ident: int, db: Session = Depends(database),
                  current_user: CreateUser = Depends(get_current_active_user)):
    delete_worker_f(ident=ident, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")



