import math
from sqlalchemy import func
from fastapi import HTTPException
from models.incomes import Incomes
from utils.db_operations import save_in_db


def get_incomes(ident, _type, start_date, end_date, page, limit, db):

    if ident > 0:
        ident_filter = Incomes.id == ident
    else:
        ident_filter = Incomes.id > 0

    if _type:
        type_filter = Incomes.type == _type
    else:
        type_filter = Incomes.id > 0

    if start_date:
        start_date_filter = Incomes.datetime >= start_date
    else:
        start_date_filter = Incomes.id > 0

    if end_date:
        end_date_filter = Incomes.datetime < end_date
    else:
        end_date_filter = Incomes.id > 0

    form = (db.query(Incomes).filter(ident_filter, type_filter, start_date_filter, end_date_filter)
            .order_by(Incomes.id.desc()))

    _total_sum = db.query(func.sum(Incomes.money)).filter(Incomes.currency == "sum",
                                                          ident_filter,
                                                          type_filter,
                                                          start_date_filter,
                                                          end_date_filter).scalar()

    total_sum = _total_sum if _total_sum is not None else 0

    _total_dollar = db.query(func.sum(Incomes.money)).filter(Incomes.currency == "dollar",
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


def create_income_f(form, db):
    new_item_db = Incomes(
        name=form.name,
        type=form.type,
        money=form.money,
        comment=form.comment,
        currency=form.currency,
    )
    save_in_db(db, new_item_db)



