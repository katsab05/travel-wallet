from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.sql import func
from app.models.base import Base, ReprMixin
from sqlalchemy.orm import relationship

class Expense(Base,ReprMixin):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    category = Column(String(50))
    description = Column(Text)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user_id = Column(ForeignKey("users.id"), nullable=True)
      
    user = relationship("User", back_populates="expenses")
    trip = relationship("Trip", back_populates="expenses")