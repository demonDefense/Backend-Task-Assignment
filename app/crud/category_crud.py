from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional, Tuple

from app.models.models import (
    Category
)
from app.schemas.schemas import (
    CategoryCreate
)

def create_category(db: Session, cat_in: CategoryCreate) -> Category:
    db_cat = Category(**cat_in.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def get_category(db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()

def list_categories(db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, cat_in: CategoryCreate) -> Optional[Category]:
    db_cat = get_category(db, category_id)
    if not db_cat:
        return None
    for key, value in cat_in.dict().items():
        setattr(db_cat, key, value)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def delete_category(db: Session, category_id: int) -> bool:
    db_cat = get_category(db, category_id)
    if not db_cat:
        return False
    db.delete(db_cat)
    db.commit()
    return True

