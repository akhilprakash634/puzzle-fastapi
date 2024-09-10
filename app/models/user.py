from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    age: int
    is_active: bool = True

    class Config:
        from_attributes = True