from db import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date


class Attendances(Base):
    __tablename__ = 'attendances'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    came_datetime = Column(DateTime, nullable=True)
    went_datetime = Column(DateTime, nullable=True)
    worker_id = Column(Integer, ForeignKey('workers.id', ondelete='CASCADE'), nullable=False)
