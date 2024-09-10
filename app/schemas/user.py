from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone_number: Optional[str] = None
    age: int = Field(..., ge=0)

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str

class User(UserBase):
    id: str

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    password: Optional[str] = None