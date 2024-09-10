from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    id: str
    text: str
    options: List[str]
    correct_answer: str
    category_id: str
    set_number: int

    class Config:
        from_attributes = True