from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentOut(BaseModel):
    id: int
    user_id: int
    trip_id: Optional[int]
    file_name: str
    file_path: str
    uploaded_at: datetime

    class Config:
        orm_mode = True
