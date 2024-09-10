from typing import List, Optional
from app.schemas.quiz import QuizSessionCreate, QuizSession
from app.schemas.question import Question, AnswerResult
from app.core.firebase import db
from app.utils.question_loader import questions
import random

class CRUDQuizSession:
    def start_new_session(self, user_id: str, category_id: str) -> QuizSession:
        category_questions = questions.get(category_id, [])
        if not category_questions:
            raise ValueError("Invalid category")
        
        session_questions = random.sample(category_questions, min(5, len(category_questions)))
        
        session_data = {
            "user_id": user_id,
            "category_id": category_id,
            "current_set": 1,
            "current_question_index": 0,
            "questions": [q.id for q in session_questions],
            "answers": [None] * len(session_questions),
            "score": 0
        }
        doc_ref = db.collection("quiz_sessions").document()
        doc_ref.set(session_data)
        return QuizSession(id=doc_ref.id, **session_data)

    def get_next_question(self, session_id: str, user_id: str) -> Optional[Question]:
        session = self.get(session_id=session_id, user_id=user_id)
        if not session:
            return None
        if session.current_question_index >= len(session.questions):
            return None
        question_id = session.questions[session.current_question_index]
        category_questions = questions.get(session.category_id, [])
        return next((q for q in category_questions if q.id == question_id), None)

    def submit_answer(self, session_id: str, user_id: str, answer: str) -> AnswerResult:
        session = self.get(session_id=session_id, user_id=user_id)
        if not session:
            raise ValueError("Invalid session")
        question_id = session.questions[session.current_question_index]
        category_questions = questions.get(session.category_id, [])
        question = next((q for q in category_questions if q.id == question_id), None)
        
        if not question:
            raise ValueError("Question not found")
        
        is_correct = question.correct_answer == answer
        if is_correct:
            session.score += 1
        
        session.answers[session.current_question_index] = answer
        session.current_question_index += 1
        
        self.update(session)
        
        return AnswerResult(is_correct=is_correct, correct_answer=question.correct_answer)

    def get(self, session_id: str, user_id: str) -> Optional[QuizSession]:
        doc = db.collection("quiz_sessions").document(session_id).get()
        if doc.exists and doc.to_dict()["user_id"] == user_id:
            data = doc.to_dict()
            data['id'] = doc.id  # Add the id to the dictionary
            return QuizSession(**data)
        return None

    def update(self, session: QuizSession) -> QuizSession:
        db.collection("quiz_sessions").document(session.id).set(session.dict())
        return session

quiz_session = CRUDQuizSession()