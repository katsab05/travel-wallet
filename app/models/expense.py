from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text
from sqlalchemy.sql import func
from app.models.base import Base, BaseModelMixin

class Expense(Base, BaseModelMixin):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    category = Column(String(50))
    description = Column(Text)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
