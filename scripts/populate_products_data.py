import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from app.models.models import Base, Category, Product, Inventory, Sale
import datetime
import random

Base.metadata.create_all(bind=engine)

categories_data = [
    {"name": "Amazon", "description": "Amazon storefront products"},
    {"name": "Walmart", "description": "Walmart storefront products"}
]

products_data = [
    {"name": "Echo Dot (4th Gen)", "category_name": "Amazon", "unit_price": 49.99},
    {"name": "Fire TV Stick 4K", "category_name": "Amazon", "unit_price": 39.99},
    {"name": "Walmart Plus Membership", "category_name": "Walmart", "unit_price": 12.95},
    {"name": "5 Gallon Water Jug", "category_name": "Walmart", "unit_price": 8.49}
]

def populate_dummy_data():
    db: Session = SessionLocal()
    try:
        category_map = {}
        for cat in categories_data:
            existing = db.query(Category).filter_by(name=cat["name"]).first()
            if not existing:
                obj = Category(name=cat["name"], description=cat.get("description"))
                db.add(obj)
                db.commit()
                db.refresh(obj)
                category_map[cat["name"]] = obj.id
            else:
                category_map[cat["name"]] = existing.id

        for prod in products_data:
            category_id = category_map.get(prod["category_name"])
            existing_prod = db.query(Product).filter_by(name=prod["name"]).first()
            if not existing_prod:
                product = Product(
                    name=prod["name"],
                    category_id=category_id,
                    unit_price=prod["unit_price"],
                    created_at=datetime.datetime.utcnow(),
                    updated_at=datetime.datetime.utcnow()
                )
                db.add(product)
                db.commit()

        print("Dummy data populated successfully.")
    finally:
        db.close()

if __name__ == '__main__':
    populate_dummy_data()

