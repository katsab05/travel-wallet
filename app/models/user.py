from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.models.base import Base, BaseModelMixin

class User(Base, BaseModelMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    password = Column(String, nullable=False)  
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    


