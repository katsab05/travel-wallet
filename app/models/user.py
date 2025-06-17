from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.models.base import Base, ReprMixin
from sqlalchemy.orm import relationship


class User(Base, ReprMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    password = Column(String, nullable=False)  
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete")

    


