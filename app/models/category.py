from pydantic import BaseModel

class Category(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True