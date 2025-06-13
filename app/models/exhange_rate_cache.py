from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.models.base import Base  

class ExchangeRateCache(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String, unique=True, nullable=False)
    rates = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

