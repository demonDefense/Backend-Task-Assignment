from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional, Tuple

from app.models.models import (
    Product
)
from app.schemas.schemas import (
    ProductCreate
)
def create_product(db: Session, prod_in: ProductCreate) -> Product:
    db_prod = Product(**prod_in.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod
    
def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()
    
def get_product_by_category(db: Session, category_id: int) -> List[Product]:
    return db.query(Product).filter(Product.category_id == category_id).all()

def list_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()
    
def update_product(db: Session, product_id: int, prod_in: ProductCreate) -> Optional[Product]:
    db_prod = get_product(db, product_id)
    if not db_prod:
        return None
    for key, value in prod_in.dict().items():
        setattr(db_prod, key, value)
    db_prod.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_prod)
    return db_prod

def delete_product(db: Session, product_id: int) -> bool:
    db_prod = get_product(db, product_id)
    if not db_prod:
        return False
    db.delete(db_prod)
    db.commit()
    return True


