from pydantic import BaseModel
from datetime import date

class TripIn(BaseModel):
    destination: str
    start_date: date
    end_date: date
    notes: str | None = None

class TripOut(TripIn):
    id: int
    class Config:
        orm_mode = True
