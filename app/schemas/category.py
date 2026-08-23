from pydantic import BaseModel
from typing import Literal, Optional


CategoryIconKey = Literal[
    "circle-dollar-sign",
    "wallet",
    "utensils",
    "shopping-bag",
    "house",
    "car",
    "bus",
    "fuel",
    "smartphone",
    "receipt",
    "heart-pulse",
    "graduation-cap",
    "gamepad-2",
    "dog",
    "baby",
    "dumbbell",
    "plane",
    "gift",
    "piggy-bank",
    "banknote",
    "briefcase-business",
    "trending-up",
    "hand-coins",
    "badge-dollar-sign",
]

class CategoryCreate(BaseModel):
    name: str
    type: str          # "income" hoặc "expense"
    color: Optional[str] = "#D9A441"
    icon: CategoryIconKey = "circle-dollar-sign"

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[CategoryIconKey] = None

class CategoryOut(BaseModel):
    id: str
    name: str
    type: str
    color: str
    icon: CategoryIconKey

    class Config:
        from_attributes = True
