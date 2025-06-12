from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from app.models.base import Base, BaseModelMixin

class TravelDocument(Base, BaseModelMixin):
    __tablename__ = "travel_documents"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String, nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TravelDocument(id={self.id}, trip_id={self.trip_id}, file_path='{self.file_path}')>"

