from pydantic import BaseModel, condecimal
from datetime import datetime


ConstrainedDecimal = condecimal(max_digits=10, decimal_places=2)

class ExpenseIn(BaseModel):
    trip_id: int
    amount: ConstrainedDecimal
    currency: str
    category: str
    description: str | None = None

class ExpenseOut(ExpenseIn):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True
