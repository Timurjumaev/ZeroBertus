from db import Base
from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    access_token = Column(String(255), nullable=True)  # Foydalanuvchi uchun access_token
    refresh_token = Column(String(255), nullable=True)  # Foydalanuvchi uchun refresh_token
    last_login = Column(DateTime, default=datetime.utcnow)  # Oxirgi login vaqti (opsional)
