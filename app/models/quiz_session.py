# app/models/quiz_session.py
from pydantic import BaseModel
from typing import List, Optional

class QuizSession(BaseModel):
    id: str
    user_id: str
    category_id: str
    current_set: int
    current_question_index: int
    questions: List[str]  # List of question IDs
    answers: List[Optional[str]]
    score: int