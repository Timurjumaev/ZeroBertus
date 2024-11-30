from models.expenses import Expenses
from models.incomes import Incomes
from models.monthlyreports import MonthlyReports
from models.salaries import Salaries
from utils.db_operations import save_in_db
from models.dailyreportsums import DailyReportSums
from utils.pagination import pagination
from sqlalchemy import cast, Date, func, text
from fastapi import HTTPException


def get_daily_report_sums(ident, status, start_date, end_date, page, limit, db):
    if ident > 0:
        ident_filter = DailyReportSums.id == ident
    else:
        ident_filter = DailyReportSums.id > 0

    if status is None:
        status_filter = DailyReportSums.id > 0
    elif status:
        status_filter = DailyReportSums.status == True
    else:
        status_filter = DailyReportSums.status == False

    if start_date:
        start_date_filter = DailyReportSums.date >= start_date
    else:
        start_date_filter = DailyReportSums.id > 0

    if end_date:
        end_date_filter = DailyReportSums.date <= end_date
    else:
        end_date_filter = DailyReportSums.id > 0

    items = (db.query(DailyReportSums).filter(ident_filter, status_filter, start_date_filter, end_date_filter)
             .order_by(DailyReportSums.id.desc()))

    return pagination(items, page, limit)


def create_daily_report_sum_f(db):
    if db.query(DailyReportSums).filter(DailyReportSums.status == True).first():
        raise HTTPException(status_code=400, detail="Sizda yakunlanmagan hisobot mavjud!")
    today_date = func.date(func.now() + text("INTERVAL 5 HOUR"))
    sandwich = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "sandwich",
            Incomes.currency == "sum",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    pena = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "pena",
            Incomes.currency == "sum",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_income = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "other",
            Incomes.currency == "sum",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    advance = (
        db.query(func.sum(Salaries.money))
        .filter(
            Salaries.type == "advance",
            Salaries.currency == "sum",
            cast(Salaries.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    usual = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "usual",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    toll = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "toll",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    food = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "food",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_expense = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )

    benefit = sandwich + pena + other_income - advance - usual - toll - food - other_expense

    new_item_db = DailyReportSums(
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


def refresh_daily_report_sum_f(db):
    if db.query(DailyReportSums).filter(DailyReportSums.status == True).first() is None:
        raise HTTPException(status_code=400, detail="Hisobot allaqachon yakunlangan!")
    today_date = func.date(func.now() + text("INTERVAL 5 HOUR"))
    sandwich = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "sandwich",
            Incomes.currency == "sum",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    pena = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "pena",
            Incomes.currency == "sum",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_income = (
        db.query(func.sum(Incomes.money))
        .filter(
            Incomes.type == "other",
            Incomes.currency == "sum",
            cast(Incomes.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    advance = (
        db.query(func.sum(Salaries.money))
        .filter(
            Salaries.type == "advance",
            Salaries.currency == "sum",
            cast(Salaries.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    usual = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    toll = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    food = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )
    other_expense = (
        db.query(func.sum(Expenses.money))
        .filter(
            Expenses.type == "other",
            Expenses.currency == "sum",
            cast(Expenses.datetime, Date) == today_date
        )
        .scalar() or 0
    )

    benefit = sandwich + pena + other_income - advance - usual - toll - food - other_expense

    db.query(DailyReportSums).filter(DailyReportSums.status == True).delete()
    db.commit()
    new_item_db = DailyReportSums(
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


def confirmation_daily_report_sum_f(db):
    current_item = db.query(DailyReportSums).filter(DailyReportSums.status == True).first()
    if current_item is None:
        raise HTTPException(status_code=400, detail="Hisobot allaqachon yakunlangan!")
    db.query(DailyReportSums).filter(DailyReportSums.status == True).update({
        DailyReportSums.status: False
    })
    db.commit()

    if db.query(MonthlyReports).filter(MonthlyReports.status == True).first():
        db.query(MonthlyReports).filter(MonthlyReports.status == True).update({
            MonthlyReports.sandwich: MonthlyReports.sandwich + current_item.sandwich,
            MonthlyReports.pena: MonthlyReports.pena + current_item.pena,
            MonthlyReports.other_income:
                MonthlyReports.other_income + current_item.other_income,
            MonthlyReports.advance: MonthlyReports.advance + current_item.advance,
            MonthlyReports.usual: MonthlyReports.usual + current_item.usual,
            MonthlyReports.toll: MonthlyReports.toll + current_item.toll,
            MonthlyReports.food: MonthlyReports.food + current_item.food,
            MonthlyReports.other_expense:
                MonthlyReports.other_expense + current_item.other_expense,
            MonthlyReports.benefit: MonthlyReports.benefit + current_item.benefit,

        })
    else:
        new_item_db = MonthlyReports(
            sandwich=current_item.sandwich,
            pena=current_item.pena,
            other_income=current_item.other_income,
            advance=current_item.advance,
            usual=current_item.usual,
            toll=current_item.toll,
            food=current_item.food,
            other_expense=current_item.other_expense,
            benefit=current_item.benefit,
        )
        save_in_db(db, new_item_db)



