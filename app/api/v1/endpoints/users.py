from fastapi import APIRouter, Depends, HTTPException
from app import crud, schemas
from app.api import deps



router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register_user(user_in: schemas.UserCreate):
    user = crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.user.create(obj_in=user_in)
    return user