import os
import sys

# Ensure project root is in path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(BASE_DIR)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from app.schemas.schemas import Category as CategorySchema, CategoryCreate
from app.crud.category_crud import *

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/categories/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_new_category(cat_in: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, cat_in)

@router.get("/categories/", response_model=List[CategorySchema])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_categories(db)

@router.get("/categories/{category_id}", response_model=CategorySchema)
def read_category(category_id: int, db: Session = Depends(get_db)):
    cat = get_category(db, category_id)
    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return cat

@router.put("/categories/{category_id}", response_model=CategorySchema)
def update_existing_category(category_id: int, cat_in: CategoryCreate, db: Session = Depends(get_db)):
    updated = update_category(db, category_id, cat_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    success = delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return None

