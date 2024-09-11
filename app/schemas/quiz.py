from pydantic import BaseModel
from typing import List, Optional

class QuizSessionCreate(BaseModel):
    category_id: str

class QuizSession(BaseModel):
    id: str
    user_id: str
    category_id: str
    current_set: int
    current_question_index: int
    questions: List[str]
    answers: List[Optional[str]]
    score: int

class AnswerSubmit(BaseModel):
    answer: str

class LeaderboardEntry(BaseModel):
    user_id: str
    username: str
    score: int