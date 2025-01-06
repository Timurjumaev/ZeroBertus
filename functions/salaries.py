from sqlalchemy import func
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.currencies import Currencies
from models.loans import Loans
from models.salaries import Salaries
from utils.db_operations import save_in_db, get_in_db
from models.workers import Workers
import math


# def get_salaries_f(ident, worker_id, _type, start_date, end_date, page, limit, db):
#
#     if ident > 0:
#         ident_filter = Salaries.id == ident
#     else:
#         ident_filter = Salaries.id > 0
#
#     if worker_id > 0:
#         worker_id_filter = Salaries.worker_id == worker_id
#     else:
#         worker_id_filter = Salaries.id > 0
#
#     if _type:
#         type_filter = Salaries.type == _type
#     else:
#         type_filter = Salaries.id > 0
#
#     if start_date:
#         start_date_filter = Salaries.datetime >= start_date
#     else:
#         start_date_filter = Salaries.id > 0
#
#     if end_date:
#         end_date_filter = Salaries.datetime < end_date
#     else:
#         end_date_filter = Salaries.id > 0
#
#     form = (db.query(Salaries).filter(ident_filter, worker_id_filter, type_filter, start_date_filter, end_date_filter)
#             .order_by(Salaries.id.desc()))
#
#     _total_sum = db.query(func.sum(Salaries.money)).filter(Salaries.currency == "sum",
#                                                            ident_filter,
#                                                            worker_id_filter,
#                                                            type_filter,
#                                                            start_date_filter,
#                                                            end_date_filter).scalar()
#
#     total_sum = _total_sum if _total_sum is not None else 0
#
#     _total_dollar = db.query(func.sum(Salaries.money)).filter(Salaries.currency == "dollar",
#                                                               ident_filter,
#                                                               type_filter,
#                                                               start_date_filter,
#                                                               end_date_filter).scalar()
#
#     total_dollar = _total_dollar if _total_dollar is not None else 0
#
#     if page < 0 or limit < 0:
#         raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
#     elif page and limit:
#         return {"total_sum": total_sum, "total_dollar": total_dollar, "current_page": page, "limit": limit,
#                 "pages": math.ceil(form.count() / limit),
#                 "data": form.offset((page - 1) * limit).limit(limit).all()}
#     else:
#         return {"data": form.all()}


def get_salaries_f(ident, _type, start_date, end_date, page, limit, db):
    ident_filter = Workers.id == ident if ident > 0 else True
    type_filter = Salaries.type == _type if _type else True
    start_date_filter = Salaries.datetime >= start_date if start_date else True
    end_date_filter = Salaries.datetime < end_date if end_date else True

    form = (db.query(Workers).options(joinedload(Workers.salaries))
            .filter(ident_filter, type_filter, start_date_filter, end_date_filter)
            .order_by(Workers.id.desc()))

    total_sum_kpi = db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "kpi", type_filter, start_date_filter, end_date_filter).scalar()

    total_sum_wdb = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "work_day_bonus", type_filter, start_date_filter, end_date_filter)
                     .scalar())

    total_sum_extra_bonus = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "extra_bonus", type_filter, start_date_filter, end_date_filter)
                             .scalar())

    total_sum_penalty = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "penalty", type_filter, start_date_filter, end_date_filter)
                     .scalar())

    total_sum_loan = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "loan", type_filter, start_date_filter, end_date_filter)
                         .scalar())

    total_sum_pension = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "pension", type_filter, start_date_filter, end_date_filter)
                      .scalar())

    total_sum_advance = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "advance", type_filter, start_date_filter, end_date_filter)
                      .scalar())

    total_sum_absolute = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "sum", Salaries.type == "absolute", type_filter, start_date_filter, end_date_filter)
                         .scalar())

    total_dollar_kpi = db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "kpi", type_filter, start_date_filter, end_date_filter).scalar()

    total_dollar_wdb = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "work_day_bonus", type_filter, start_date_filter, end_date_filter)
                     .scalar())

    total_dollar_extra_bonus = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "extra_bonus", type_filter, start_date_filter, end_date_filter)
                             .scalar())

    total_dollar_penalty = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "penalty", type_filter, start_date_filter, end_date_filter)
                         .scalar())

    total_dollar_loan = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "loan", type_filter, start_date_filter, end_date_filter)
                      .scalar())

    total_dollar_pension = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "pension", type_filter, start_date_filter, end_date_filter)
                         .scalar())

    total_dollar_advance = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "advance", type_filter, start_date_filter, end_date_filter)
                         .scalar())

    total_dollar_absolute = (db.query(func.coalesce(func.sum(Salaries.money), 0)).filter(
        Salaries.currency == "dollar", Salaries.type == "absolute", type_filter, start_date_filter, end_date_filter)
                          .scalar())

    if page <= 0 or limit <= 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik yoki 0 ga teng bo'lishi mumkin emas")

    if page and limit:
        return {
            "total_sum_kpi": total_sum_kpi,
            "total_sum_wdb": total_sum_wdb,
            "total_sum_extra_bonus": total_sum_extra_bonus,
            "total_sum_penalty": total_sum_penalty,
            "total_sum_loan": total_sum_loan,
            "total_sum_pension": total_sum_pension,
            "total_sum_advance": total_sum_advance,
            "total_sum_absolute": total_sum_absolute,
            "total_dollar_kpi": total_dollar_kpi,
            "total_dollar_wdb": total_dollar_wdb,
            "total_dollar_extra_bonus": total_dollar_extra_bonus,
            "total_dollar_penalty": total_dollar_penalty,
            "total_dollar_loan": total_dollar_loan,
            "total_dollar_pension": total_dollar_pension,
            "total_dollar_advance": total_dollar_advance,
            "total_dollar_absolute": total_dollar_absolute,
            "total_sum_expense_for_salary": total_sum_absolute + total_sum_advance,
            "total_dollar_expense_for_salary": total_dollar_absolute + total_dollar_advance,
            "current_page": page,
            "limit": limit,
            "pages": math.ceil(form.count() / limit),
            "data": form.offset((page - 1) * limit).limit(limit).all()
        }
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
    elif form.type == "loan":
        db.query(Workers).filter(Workers.id == form.worker_id).update({
            Workers.balance: Workers.balance - money,
        })
        db.query(Loans).filter(Loans.worker_id == form.worker_id).update({
            Loans.residual: Loans.residual - money
        })
        db.commit()
    else:
        db.query(Workers).filter(Workers.id == form.worker_id).update({
            Workers.balance: Workers.balance - money
        })
        db.commit()


def delete_salary_f(ident, db):
    get_in_db(db, Salaries, ident)
    db.query(Salaries).filter(Salaries.id == ident).delete()
    db.commit()


