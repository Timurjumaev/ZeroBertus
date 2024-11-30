from db import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, func, text


class Currencies(Base):
    __tablename__ = 'currencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, default=func.date(func.now() + text("INTERVAL 5 HOUR")))
    status = Column(Boolean, nullable=False, default=True)


