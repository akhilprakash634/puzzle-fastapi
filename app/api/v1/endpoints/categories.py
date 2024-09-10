from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_user)
):
    return crud.category.create(obj_in=category)

@router.get("/", response_model=List[schemas.Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user)
):
    categories = crud.category.get_multi(skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    category = crud.category.get(category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: str,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(deps.get_current_user)
):
    category = crud.category.get(category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.update(category_id=category_id, obj_in=category_in)
    return category

@router.delete("/{category_id}", response_model=schemas.Category)
def delete_category(
    category_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    category = crud.category.get(category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.category.remove(category_id=category_id)
    return category