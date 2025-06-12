from sqlalchemy import Column, Integer, String, Date, Text
from app.models.base import Base, BaseModelMixin

class Trip(Base, BaseModelMixin):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)

