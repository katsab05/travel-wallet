from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base, ReprMixin

class TravelDocument(Base, ReprMixin):
    __tablename__ = "travel_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # local path or S3 URL
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
