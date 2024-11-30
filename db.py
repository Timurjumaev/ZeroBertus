from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql

engine = create_engine('mysql+pymysql://root:Tjumaev#02@localhost:3306/zerobertus')
SessionLocal = sessionmaker(bind=engine)


Base = declarative_base()


def database():
    db = SessionLocal()
    try:
        yield db
    # except SQLAlchemyError as e:
    #     db.rollback()
    #     raise RuntimeError("Database transaction failed") from e
    finally:
        db.close()
