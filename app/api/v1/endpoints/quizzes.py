from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app import crud, models, schemas
from app.api import deps
from app.utils.question_loader import questions

router = APIRouter()

@router.get("/categories", response_model=List[str])
def get_categories(current_user: models.User = Depends(deps.get_current_user)):
    return list(questions.keys())

@router.post("/start", response_model=schemas.QuizSession)
def start_quiz(
    quiz_data: schemas.QuizSessionCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    if quiz_data.category_id not in questions:
        raise HTTPException(status_code=400, detail="Invalid category")
    return crud.quiz_session.start_new_session(user_id=current_user.id, category_id=quiz_data.category_id)

@router.get("/next-question", response_model=schemas.Question)
def get_next_question(
    session_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    question = crud.quiz_session.get_next_question(session_id=session_id, user_id=current_user.id)
    if not question:
        raise HTTPException(status_code=404, detail="No more questions or invalid session")
    return question

@router.post("/submit-answer", response_model=schemas.AnswerResult)
def submit_answer(
    session_id: str,
    answer: schemas.AnswerSubmit,
    current_user: models.User = Depends(deps.get_current_user)
):
    try:
        return crud.quiz_session.submit_answer(session_id=session_id, user_id=current_user.id, answer=answer.answer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))