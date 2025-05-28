import os
import sys

# Ensure project root is in path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(BASE_DIR)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from app.crud.crud import (
    list_products, get_product, create_product, get_product_by_category
)
from app.schemas.schemas import Product, ProductCreate, Category

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_new_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    # Ensure category exists
    from app.crud.crud import get_category
    category = get_category(db, product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    return create_product(db, product_in)

@router.get("/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    prod = get_product(db, product_id)
    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return prod

@router.get("/category/{category_id}", response_model=List[Product])
def read_products_by_category(category_id: int, db: Session = Depends(get_db)):
    prods = get_product_by_category(db, category_id)
    if not prods:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return prods

