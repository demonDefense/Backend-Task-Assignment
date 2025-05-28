import os
import sys

# Ensure project root is in path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(BASE_DIR)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from app.crud.product_crud import *
from app.schemas.schemas import Product as ProductSchema, ProductCreate, Category
from app.crud.category_crud import get_category

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_new_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    # If Category exist then add product
    category = get_category(db, product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    return create_product(db, product_in)

@router.get("/", response_model=List[ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_products(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    prod = get_product(db, product_id)
    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return prod

@router.get("/category/{category_id}", response_model=List[ProductSchema])
def read_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return get_product_by_category(db, category_id)
    
@router.put("/products/{product_id}", response_model=ProductSchema)
def update_existing_product(product_id: int, product_in: ProductCreate, db: Session = Depends(get_db)):
    # If Category exist then update product
    category = get_category(db, product_in.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found"
        )
    updated = update_product(db, product_id, product_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return None

