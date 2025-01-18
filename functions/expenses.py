import math
from fastapi import HTTPException
from models.expenses import Expenses
from utils.db_operations import save_in_db, get_in_db
from sqlalchemy import func, text


def get_expenses(ident, search, _type, start_date, end_date, page, limit, db):

    if ident > 0:
        ident_filter = Expenses.id == ident
    else:
        ident_filter = Expenses.id > 0

    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Expenses.comment.like(search_formatted)
    else:
        search_filter = Expenses.id > 0

    if _type:
        type_filter = Expenses.type == _type
    else:
        type_filter = Expenses.id > 0

    if start_date:
        start_date_filter = Expenses.datetime >= start_date
    else:
        start_date_filter = Expenses.id > 0

    if end_date:
        end_date_filter = Expenses.datetime < end_date
    else:
        end_date_filter = Expenses.id > 0

    form = (db.query(Expenses).filter(ident_filter, search_filter, type_filter, start_date_filter, end_date_filter)
            .order_by(Expenses.id.desc()))

    _total_sum = db.query(func.sum(Expenses.money)).filter(Expenses.currency == "sum",
                                                           ident_filter,
                                                           type_filter,
                                                           start_date_filter,
                                                           end_date_filter).scalar()

    total_sum = _total_sum if _total_sum is not None else 0

    _total_dollar = db.query(func.sum(Expenses.money)).filter(Expenses.currency == "dollar",
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


def create_expense_f(form, db):
    if form.datetime:
        dt = form.datetime
    else:
        dt = func.now() + text("INTERVAL 5 HOUR")
    new_item_db = Expenses(
        type=form.type,
        money=form.money,
        comment=form.comment,
        currency=form.currency,
        datetime=dt
    )
    save_in_db(db, new_item_db)


def delete_expense_f(ident, db):
    get_in_db(db, Expenses, ident)
    db.query(Expenses).filter(Expenses.id == ident).delete()
    db.commit()




