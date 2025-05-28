from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional, Tuple

from app.models.models import (
    Category, Product
)
from app.schemas.schemas import (
    CategoryCreate, ProductCreate
)


# --- Category & Product CRUD ---

def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(db: Session, cat_in: CategoryCreate) -> Category:
    db_cat = Category(**cat_in.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def list_categories(db: Session) -> List[Category]:
    return db.query(Category).all()

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()
    
def get_product_by_category(db: Session, category_id: int) -> List[Product]:
    return db.query(Product).filter(Product.category_id == category_id).all()

def create_product(db: Session, prod_in: ProductCreate) -> Product:
    db_prod = Product(**prod_in.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


def list_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


