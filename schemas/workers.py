from enum import Enum
from pydantic import BaseModel, Field, validator
from db import SessionLocal
from models.workers import Workers
from utils.db_operations import get_in_db

db = SessionLocal()


class Part(str, Enum):
    office = "office"
    sandwich = "sandwich"
    peno_cutting = "peno_cutting"
    peno_making = "peno_making"
    other = "other"


class CreateWorker(BaseModel):
    name: str
    workdays: int
    fixed: int
    part: Part

    @validator('name')
    def name_validate(cls, name):
        validate_my = db.query(Workers).filter(
            Workers.name == name,
        ).count()

        if validate_my != 0:
            raise ValueError('Bunday ism avval ro`yxatga olingan!')
        return name


class UpdateWorker(BaseModel):
    id: int = Field(..., gt=0)
    name: str
    workdays: int
    fixed: int
    part: Part

    @validator('name')
    def name_validate(cls, name, values):
        validate_my = db.query(Workers).filter(
            Workers.name == name,
        ).count()

        the_worker = get_in_db(db, Workers, values['id'])

        if validate_my != 0 and name != the_worker.name:
            raise ValueError('Bunday ism avval ro`yxatga olingan!')
        return name

