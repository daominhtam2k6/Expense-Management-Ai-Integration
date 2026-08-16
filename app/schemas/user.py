from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)
    email: Optional[EmailStr] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
