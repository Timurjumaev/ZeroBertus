from fastapi import APIRouter
from routes.login import login_router
from routes.users import users_router
from routes.workers import workers_router
from routes.loans import loans_router
from routes.currencies import currencies_router
from routes.salaries import salaries_router
from routes.incomes import incomes_router
from routes.expenses import expenses_router
from routes.dailyreportsums import daily_report_sums_router
from routes.dailyreportdollars import daily_report_dollars_router
from routes.monthlyreports import monthly_reports_router
from routes.attendances import attendances_router
from routes.daily_data import daily_data_router


api = APIRouter()


api.include_router(login_router)
api.include_router(users_router)
api.include_router(workers_router)
api.include_router(loans_router)
api.include_router(currencies_router)
api.include_router(salaries_router)
api.include_router(incomes_router)
api.include_router(expenses_router)
api.include_router(daily_report_sums_router)
api.include_router(daily_report_dollars_router)
api.include_router(monthly_reports_router)
api.include_router(attendances_router)
api.include_router(daily_data_router)

