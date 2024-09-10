from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, quizzes

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
# api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
# api_router.include_router(questions.router, prefix="/questions", tags=["questions"])