from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class Type(str, Enum):
    sandwich = "sandwich"
    pena = "pena"
    other = "other"


class Currency(str, Enum):
    sum = "sum"
    dollar = "dollar"


class CreateIncome(BaseModel):
    name: str
    type: Type
    money: int
    comment: str
    currency: Currency
    datetime: datetime
