from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from db import database  # Sessionni olish uchun funksiyangiz
from models.incomes import Incomes
from models.expenses import Expenses
from models.salaries import Salaries
from models.workers import Workers
from routes.login import get_current_active_user
from schemas.users import CreateUser

daily_data_router = APIRouter(
    prefix="/daily_data",
    tags=["Daily Data Operation"]
)


@daily_data_router.get("/all-data/")
def get_all_data(
    current_date: str = Query(None, description="Filter by date in 'YYYY-MM-DD' format"),
    db: Session = Depends(database),
    current_user: CreateUser = Depends(get_current_active_user)
):
    def process_table(query_results, table_name, include_worker_name=False):
        data = {}
        detailed_list = []
        total_sum = 0
        total_dollar = 0

        for row in query_results:
            key_sum = f"total_money_sum_{row.type}_{table_name}"
            key_dollar = f"total_money_dollar_{row.type}_{table_name}"

            if key_sum not in data:
                data[key_sum] = 0
            if key_dollar not in data:
                data[key_dollar] = 0

            if row.currency == "sum":
                data[key_sum] += row.total_money
                total_sum += row.total_money
            elif row.currency == "dollar":
                data[key_dollar] += row.total_money
                total_dollar += row.total_money

            detailed_data = {
                "id": row.id,
                "type": row.type,
                "amount": row.total_money,
                "currency": row.currency,
                "datetime": row.datetime,
                "comment": row.comment
            }

            if hasattr(row, "name"):
                detailed_data["name"] = row.name

            if include_worker_name:
                detailed_data["worker_name"] = row.worker_name

            detailed_list.append(detailed_data)

        data[f"finally_sum_{table_name}"] = total_sum
        data[f"finally_dollar_{table_name}"] = total_dollar
        data[f"{table_name}"] = detailed_list

        return data

    # Filtr uchun datetime ustunini date formatiga o'girish
    date_filter = func.date(Incomes.datetime) == current_date if current_date else True

    # Incomes uchun
    incomes_query = db.query(
        Incomes.id,
        Incomes.type,
        func.sum(Incomes.money).label("total_money"),
        Incomes.currency,
        Incomes.datetime,
        Incomes.comment,
        Incomes.name
    ).filter(date_filter).group_by(Incomes.id, Incomes.type, Incomes.currency, Incomes.datetime, Incomes.comment, Incomes.name).all()
    incomes_data = process_table(incomes_query, "incomes")

    # Expenses uchun
    date_filter = func.date(Expenses.datetime) == current_date if current_date else True
    expenses_query = db.query(
        Expenses.id,
        Expenses.type,
        func.sum(Expenses.money).label("total_money"),
        Expenses.currency,
        Expenses.datetime,
        Expenses.comment
    ).filter(date_filter).group_by(Expenses.id, Expenses.type, Expenses.currency, Expenses.datetime, Expenses.comment).all()
    expenses_data = process_table(expenses_query, "expenses")

    # Salaries uchun
    date_filter = func.date(Salaries.datetime) == current_date if current_date else True
    salaries_query = db.query(
        Salaries.id,
        Salaries.type,
        func.sum(Salaries.money).label("total_money"),
        Salaries.currency,
        Salaries.datetime,
        Salaries.comment,
        Workers.name.label("worker_name")
    ).join(Workers, Workers.id == Salaries.worker_id).filter(Salaries.type == "advance", date_filter).group_by(
        Salaries.id, Salaries.type, Salaries.currency, Salaries.datetime, Salaries.comment, Workers.name
    ).all()
    salaries_data = process_table(salaries_query, "salaries", include_worker_name=True)

    # Yakuniy foyda (benefit) hisoblash
    finally_sum_incomes = incomes_data.get("finally_sum_incomes", 0)
    finally_dollar_incomes = incomes_data.get("finally_dollar_incomes", 0)

    finally_sum_expenses = expenses_data.get("finally_sum_expenses", 0)
    finally_dollar_expenses = expenses_data.get("finally_dollar_expenses", 0)

    finally_sum_salaries = salaries_data.get("finally_sum_salaries", 0)
    finally_dollar_salaries = salaries_data.get("finally_dollar_salaries", 0)

    finally_sum_benefit = finally_sum_incomes - (finally_sum_expenses + finally_sum_salaries)
    finally_dollar_benefit = finally_dollar_incomes - (finally_dollar_expenses + finally_dollar_salaries)

    result = {
        "finally_sum_benefit": finally_sum_benefit,
        "finally_dollar_benefit": finally_dollar_benefit,
        **incomes_data,
        **expenses_data,
        **salaries_data
    }

    return result
