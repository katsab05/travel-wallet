from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from app.models.base import Base, ReprMixin
from sqlalchemy.orm import relationship

class Trip(Base, ReprMixin):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)

    user_id = Column(ForeignKey("users.id"), nullable=True)  
    user = relationship("User", back_populates="trips")

    expenses = relationship("Expense", back_populates="trip", cascade="all, delete")
