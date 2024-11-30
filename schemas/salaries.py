from enum import Enum
from pydantic import BaseModel


class Type(str, Enum):
    kpi = "kpi"
    work_day_bonus = "work_day_bonus"
    extra_bonus = "extra_bonus"
    penalty = "penalty"
    loan = "loan"
    pension = "pension"
    advance = "advance"
    absolute = "absolute"


class Currency(str, Enum):
    sum = "sum"
    dollar = "dollar"


class CreateSalary(BaseModel):
    type: Type
    worker_id: int
    money: int
    comment: str
    currency: Currency



