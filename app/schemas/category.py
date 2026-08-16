from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    type: str          # "income" hoặc "expense"
    color: Optional[str] = "#D9A441"

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None

class CategoryOut(BaseModel):
    id: str
    name: str
    type: str
    color: str

    class Config:
        from_attributes = True
