from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Question)
def create_question(
    question: schemas.QuestionCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    return crud.question.create(obj_in=question)

@router.get("/", response_model=List[schemas.Question])
def read_questions(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user)
):
    questions = crud.question.get_multi(skip=skip, limit=limit)
    return questions

@router.get("/{question_id}", response_model=schemas.Question)
def read_question(
    question_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    question = crud.question.get(question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=schemas.Question)
def update_question(
    question_id: str,
    question_in: schemas.QuestionUpdate,
    current_user: models.User = Depends(deps.get_current_user)
):
    question = crud.question.get(question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    question = crud.question.update(question_id=question_id, obj_in=question_in)
    return question

@router.delete("/{question_id}", response_model=schemas.Question)
def delete_question(
    question_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    question = crud.question.get(question_id=question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    question = crud.question.remove(question_id=question_id)
    return question