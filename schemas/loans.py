from pydantic import BaseModel


class CreateLoan(BaseModel):
    total: int
    worker_id: int



