from pydantic import BaseModel, Field
from typing import Optional


class AttractionBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    category: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class AttractionCreate(AttractionBase):
    pass


class AttractionOut(AttractionBase):
    id: int

    class Config:
        orm_mode = True
