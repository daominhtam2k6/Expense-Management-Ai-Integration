from sqlalchemy import Column, String, ForeignKey
from app.database import Base
import uuid

class Category(Base):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)   # "income" hoặc "expense"
    color = Column(String, nullable=False, default="#D9A441")
