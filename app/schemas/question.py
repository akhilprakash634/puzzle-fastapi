from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    id: str
    text: str
    options: List[str]
    correct_answer: str
    category: str
    set_number: int

class AnswerResult(BaseModel):
    is_correct: bool
    correct_answer: str