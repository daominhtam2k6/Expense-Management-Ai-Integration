from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)
    email: EmailStr

class UserLogin(BaseModel):
    identifier: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6)  # khớp rule đăng ký hiện tại (UserRegister)

class MessageResponse(BaseModel):
    message: str
