from db import Base
from sqlalchemy import Column, Integer, String, DateTime, func, text


class Expenses(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255), nullable=False)
    money = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=True)
    datetime = Column(DateTime, nullable=False, default=func.now() + text("INTERVAL 5 HOUR"))
    currency = Column(String(255), nullable=False)
