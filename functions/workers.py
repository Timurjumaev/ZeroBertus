from sqlalchemy.orm import joinedload
from utils.db_operations import save_in_db, get_in_db
from models.workers import Workers
from utils.pagination import pagination
from fastapi import HTTPException


def get_workers(ident, search, part, page, limit, db):

    if ident > 0:
        ident_filter = Workers.id == ident
    else:
        ident_filter = Workers.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Workers.name.like(search_formatted)
    else:
        search_filter = Workers.id > 0

    if part:
        part_filter = Workers.part == part
    else:
        part_filter = Workers.id > 0

    items = db.query(Workers).options(joinedload(Workers.attendances),
                                      joinedload(Workers.salaries),
                                      joinedload(Workers.loans))\
        .filter(ident_filter, search_filter, part_filter).order_by(Workers.name)

    return pagination(items, page, limit)


def create_worker_f(form, db):
    if db.query(Workers).filter(Workers.name == form.name).first():
        raise HTTPException(status_code=400, detail="Bunday ismli ishchi avval ro'yxatga olingan!")
    new_item_db = Workers(
        name=form.name,
        workdays=form.workdays,
        fixed=form.fixed,
        part=form.part
    )
    save_in_db(db, new_item_db)


def update_worker_f(form, db):
    get_in_db(db, Workers, form.id)
    db.query(Workers).filter(Workers.id == form.id).update({
        Workers.name: form.name,
        Workers.workdays: form.workdays,
        Workers.fixed: form.fixed,
        Workers.part: form.part,
    })
    db.commit()


def delete_worker_f(ident, db):
    get_in_db(db, Workers, ident)
    db.query(Workers).filter(Workers.id == ident).delete()
    db.commit()


