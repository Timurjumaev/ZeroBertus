from sqlalchemy import func
from fastapi import HTTPException
from models.currencies import Currencies
from models.salaries import Salaries
from utils.db_operations import save_in_db, get_in_db
from models.workers import Workers
import math


def get_salaries_f(ident, worker_id, _type, start_date, end_date, page, limit, db):

    if ident > 0:
        ident_filter = Salaries.id == ident
    else:
        ident_filter = Salaries.id > 0

    if worker_id > 0:
        worker_id_filter = Salaries.worker_id == worker_id
    else:
        worker_id_filter = Salaries.id > 0

    if _type:
        type_filter = Salaries.type == _type
    else:
        type_filter = Salaries.id > 0

    if start_date:
        start_date_filter = Salaries.datetime >= start_date
    else:
        start_date_filter = Salaries.id > 0

    if end_date:
        end_date_filter = Salaries.datetime < end_date
    else:
        end_date_filter = Salaries.id > 0

    form = (db.query(Salaries).filter(ident_filter, worker_id_filter, type_filter, start_date_filter, end_date_filter)
            .order_by(Salaries.id.desc()))

    _total_sum = db.query(func.sum(Salaries.money)).filter(Salaries.currency == "sum",
                                                           ident_filter,
                                                           worker_id_filter,
                                                           type_filter,
                                                           start_date_filter,
                                                           end_date_filter).scalar()

    total_sum = _total_sum if _total_sum is not None else 0

    _total_dollar = db.query(func.sum(Salaries.money)).filter(Salaries.currency == "dollar",
                                                              ident_filter,
                                                              type_filter,
                                                              start_date_filter,
                                                              end_date_filter).scalar()

    total_dollar = _total_dollar if _total_dollar is not None else 0

    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    elif page and limit:
        return {"total_sum": total_sum, "total_dollar": total_dollar, "current_page": page, "limit": limit,
                "pages": math.ceil(form.count() / limit),
                "data": form.offset((page - 1) * limit).limit(limit).all()}
    else:
        return {"data": form.all()}


def create_salary_f(form, db):
    get_in_db(db, Workers, form.worker_id)
    new_item_db = Salaries(
        type=form.type,
        money=form.money,
        comment=form.comment,
        currency=form.currency,
        worker_id=form.worker_id
    )
    save_in_db(db, new_item_db)
    current_currency_amount = (
        db.query(Currencies.price)
        .filter(Currencies.status == True)
        .scalar()
    )
    if current_currency_amount is None:
        raise HTTPException(status_code=400, detail="Valyuta kursi belgilanmagan!")
    if form.currency == "sum":
        money = form.money
    else:
        money = form.money * current_currency_amount
    if form.type == "kpi" or form.type == "work_day_bonus" or form.type == "extra_bonus":
        db.query(Workers).filter(Workers.id == form.worker_id).update({
            Workers.balance: Workers.balance + money
        })
        db.commit()
    else:
        db.query(Workers).filter(Workers.id == form.worker_id).update({
            Workers.balance: Workers.balance - money
        })
        db.commit()


