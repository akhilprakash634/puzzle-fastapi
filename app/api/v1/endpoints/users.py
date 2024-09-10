from fastapi import APIRouter, Depends, HTTPException
from app import crud, schemas, models
from app.api import deps



router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register_user(user_in: schemas.UserCreate):
    user = crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.user.create(obj_in=user_in)
    return user

@router.get("/me/stats", response_model=schemas.UserStats)
def get_user_stats(current_user: models.User = Depends(deps.get_current_user)):
    return crud.user.get_user_stats(user_id=current_user.id)
