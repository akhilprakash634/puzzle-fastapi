from typing import List, Optional
from app.schemas.question import Question
from app.core.firebase import db

class CRUDQuestion:
    def create(self, obj_in: QuestionCreate) -> Question:
        doc_ref = db.collection("questions").document()
        question_data = obj_in.dict()
        doc_ref.set(question_data)
        return Question(id=doc_ref.id, **question_data)

    def get(self, question_id: str) -> Optional[Question]:
        doc = db.collection("questions").document(question_id).get()
        if doc.exists:
            return Question(id=doc.id, **doc.to_dict())
        return None

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Question]:
        docs = db.collection("questions").limit(limit).offset(skip).stream()
        return [Question(id=doc.id, **doc.to_dict()) for doc in docs]

    def update(self, question_id: str, obj_in: QuestionUpdate) -> Optional[Question]:
        question = self.get(question_id)
        if not question:
            return None
        update_data = obj_in.dict(exclude_unset=True)
        db.collection("questions").document(question_id).update(update_data)
        return self.get(question_id)

    def delete(self, question_id: str) -> bool:
        question = self.get(question_id)
        if not question:
            return False
        db.collection("questions").document(question_id).delete()
        return True

question = CRUDQuestion()