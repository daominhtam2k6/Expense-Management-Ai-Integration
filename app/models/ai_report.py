from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import uuid

class AIReport(Base):
    __tablename__ = "ai_reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    summary = Column(Text, nullable=True)
    suggestions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
