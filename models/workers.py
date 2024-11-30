from sqlalchemy.orm import relationship
from db import Base
from sqlalchemy import Column, String, Integer
from models.attendances import Attendances
from models.loans import Loans
from models.salaries import Salaries


class Workers(Base):
    __tablename__ = 'workers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    workdays = Column(Integer, nullable=False)
    fixed = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False, default=0)
    part = Column(String(255), nullable=False)

    attendances = relationship(Attendances)
    salaries = relationship(Salaries)
    loans = relationship(Loans)



