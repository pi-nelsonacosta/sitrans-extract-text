# Archivo: app/models/extraction_request.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.db.base import Base

class ExtractionRequest(Base):
    __tablename__ = "extraction_requests"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)  # Especifica una longitud (e.g., 255)
    status = Column(String(50), nullable=False)  # Especifica una longitud (e.g., 50)
    extracted_text = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
