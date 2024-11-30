from db import Base
from sqlalchemy import Column, Integer, Date, Boolean, func, text


class DailyReportSums(Base):
    __tablename__ = 'daily_report_sums'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sandwich = Column(Integer, nullable=False, default=0)
    pena = Column(Integer, nullable=False, default=0)
    other_income = Column(Integer, nullable=False, default=0)
    advance = Column(Integer, nullable=False, default=0)
    usual = Column(Integer, nullable=False, default=0)
    toll = Column(Integer, nullable=False, default=0)
    food = Column(Integer, nullable=False, default=0)
    other_expense = Column(Integer, nullable=False, default=0)
    benefit = Column(Integer, nullable=False, default=0)
    date = Column(Date, nullable=False, default=func.date(func.now() + text("INTERVAL 5 HOUR")))
    status = Column(Boolean, nullable=False, default=True)
    