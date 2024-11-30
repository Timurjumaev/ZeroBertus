from enum import Enum
from pydantic import BaseModel


class Type(str, Enum):
    usual = "usual"
    toll = "toll"
    food = "food"
    other = "other"


class Currency(str, Enum):
    sum = "sum"
    dollar = "dollar"


class CreateExpense(BaseModel):
    type: Type
    money: int
    comment: str
    currency: Currency



