import os
import sys
import random
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from database import SessionLocal, engine
from app.models.models import Base, Product, Inventory

Base.metadata.create_all(bind=engine)

num_entries = 50
min_qty = 0
max_qty = 500
low_threshold = 20

def populate_inventory_data():
    db = SessionLocal()
    try:
        product_ids = [p.id for p in db.query(Product).all()]
        if not product_ids:
            print("No products found. Please populate products first.")
            return

        for pid in product_ids:
            qty = random.randint(min_qty, max_qty)
            inv = Inventory(
                product_id=pid,
                quantity_on_hand=qty,
                low_stock_threshold=low_threshold,
                last_updated=datetime.datetime.utcnow()
            )
            db.merge(inv)
        db.commit()
        print(f"Inventory seeded for {len(product_ids)} products.")
    finally:
        db.close()

if __name__ == '__main__':
    populate_inventory_data()
