from db import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func, text


class Loans(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(Integer, nullable=False)
    residual = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False, default=func.now() + text("INTERVAL 5 HOUR"))
    worker_id = Column(Integer, ForeignKey('workers.id', ondelete='CASCADE'), nullable=False)
