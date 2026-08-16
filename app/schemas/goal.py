from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
from typing import Optional

class GoalCreate(BaseModel):
    name: str
    target_amount: Decimal = Field(gt=0)
    deadline: Optional[date] = None

class GoalItemCreate(BaseModel):
    name: str
    cost: Decimal = Field(gt=0)

class GoalItemOut(BaseModel):
    id: str
    name: str
    cost: Decimal
    is_purchased: bool
    class Config:
        from_attributes = True

class GoalTxCreate(BaseModel):
    amount: Decimal = Field(gt=0)
    note: Optional[str] = None

class GoalOut(BaseModel):
    id: str
    name: str
    target_amount: Decimal
    deadline: Optional[date] = None
    status: str
    current_amount: Decimal = 0
    items: list[GoalItemOut] = []
    class Config:
        from_attributes = True
