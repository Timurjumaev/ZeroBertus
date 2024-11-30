from models.currencies import Currencies
from models.expenses import Expenses
from models.incomes import Incomes
from models.monthlyreports import MonthlyReports
from models.salaries import Salaries
from utils.db_operations import save_in_db
from models.dailyreportdollars import DailyReportDollars
from utils.pagination import pagination
from sqlalchemy import cast, Date, func, text
from fastapi import HTTPException


def get_daily_report_dollars(ident, status, start_date, end_date, page, limit, db):

    if ident > 0:
        ident_filter = DailyReportDollars.id == ident
    else:
        ident_filter = DailyReportDollars.id > 0

    if status is None:
        status_filter = DailyReportDollars.id > 0
    elif status:
        status_filter = DailyReportDollars.status == True
    else:
        status_filter = DailyReportDollars.status == False

    if start_date:
        start_date_filter = DailyReportDollars.date >= start_date
    else:
        start_date_filter = DailyReportDollars.id > 0

    if end_date:
        end_date_filter = DailyReportDollars.date <= end_date
    else:
        end_date_filter = DailyReportDollars.id > 0

    items = (db.query(DailyReportDollars).filter(ident_filter, status_filter, start_date_filter, end_date_filter)
             .order_by(DailyReportDollars.id.desc()))

    return pagination(items, page, limit)


def create_daily_report_dollar_f(db):
    if db.query(DailyReportDollars).filter(DailyReportDollars.status == True).first():
        raise HTTPException(status_code=400, detail="Sizda yakunlanmagan hisobot mavjud!")
    today_date = func.date(func.now() + text("INTERVAL 5 HOUR"))
    sandwich = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "sandwich",
            Incomes.currency == "dollar",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    pena = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "pena",
            Incomes.currency == "dollar",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_income = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "other",
            Incomes.currency == "dollar",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    advance = (
        db.query(func.sum(Salaries.money))
        .filter(
            Salaries.type == "advance",
            Salaries.currency == "dollar",
            cast(Salaries.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    usual = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "usual",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    toll = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "toll",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    food = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "food",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_expense = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )

    benefit = sandwich + pena + other_income - advance - usual - toll - food - other_expense

    new_item_db = DailyReportDollars(
        sandwich=sandwich,
        pena=pena,
        other_income=other_income,
        advance=advance,
        usual=usual,
        toll=toll,
        food=food,
        other_expense=other_expense,
        benefit=benefit
    )
    save_in_db(db, new_item_db)


def refresh_daily_report_dollar_f(db):
    if db.query(DailyReportDollars).filter(DailyReportDollars.status == True).first() is None:
        raise HTTPException(status_code=400, detail="Hisobot allaqachon yakunlangan!")
    today_date = func.date(func.now() + text("INTERVAL 5 HOUR"))
    sandwich = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "sandwich",
            Incomes.currency == "dollar",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    pena = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "pena",
            Incomes.currency == "dollar",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_income = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "other",
            Incomes.currency == "dollar",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    advance = (
        db.query(func.sum(Salaries.money))
        .filter(
            Salaries.type == "advance",
            Salaries.currency == "dollar",
            cast(Salaries.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    usual = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    toll = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    food = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_expense = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "dollar",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )

    benefit = sandwich + pena + other_income - advance - usual - toll - food - other_expense

    db.query(DailyReportDollars).filter(DailyReportDollars.status == True).delete()
    db.commit()
    new_item_db = DailyReportDollars(
        sandwich=sandwich,
        pena=pena,
        other_income=other_income,
        advance=advance,
        usual=usual,
        toll=toll,
        food=food,
        other_expense=other_expense,
        benefit=benefit
    )
    save_in_db(db, new_item_db)


def confirmation_daily_report_dollar_f(db):
    current_item = db.query(DailyReportDollars).filter(DailyReportDollars.status == True).first()
    if current_item is None:
        raise HTTPException(status_code=400, detail="Hisobot allaqachon yakunlangan!")
    db.query(DailyReportDollars).filter(DailyReportDollars.status == True).update({
        DailyReportDollars.status: False
    })
    db.commit()
    current_currency_amount = (
        db.query(Currencies.price)
        .filter(Currencies.status == True)
        .scalar() or 0
    )

    if db.query(MonthlyReports).filter(MonthlyReports.status == True).first():
        db.query(MonthlyReports).filter(MonthlyReports.status == True).update({
            MonthlyReports.sandwich: MonthlyReports.sandwich + current_item.sandwich * current_currency_amount,
            MonthlyReports.pena: MonthlyReports.pena + current_item.pena * current_currency_amount,
            MonthlyReports.other_income:
                MonthlyReports.other_income + current_item.other_income * current_currency_amount,
            MonthlyReports.advance: MonthlyReports.advance + current_item.advance * current_currency_amount,
            MonthlyReports.usual: MonthlyReports.usual + current_item.usual * current_currency_amount,
            MonthlyReports.toll: MonthlyReports.toll + current_item.toll * current_currency_amount,
            MonthlyReports.food: MonthlyReports.food + current_item.food * current_currency_amount,
            MonthlyReports.other_expense:
                MonthlyReports.other_expense + current_item.other_expense * current_currency_amount,
            MonthlyReports.benefit: MonthlyReports.benefit + current_item.benefit * current_currency_amount

        })
    else:
        new_item_db = MonthlyReports(
            sandwich=current_item.sandwich * current_currency_amount,
            pena=current_item.pena * current_currency_amount,
            other_income=current_item.other_income * current_currency_amount,
            advance=current_item.advance * current_currency_amount,
            usual=current_item.usual * current_currency_amount,
            toll=current_item.toll * current_currency_amount,
            food=current_item.food * current_currency_amount,
            other_expense=current_item.other_expense * current_currency_amount,
            benefit=current_item.benefit * current_currency_amount
        )
        save_in_db(db, new_item_db)



