from pydantic import BaseModel


class CreateCurrency(BaseModel):
    price: int



