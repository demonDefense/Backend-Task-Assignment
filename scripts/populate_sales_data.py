#!/usr/bin/env python
import os
import sys
import random
import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from database import SessionLocal, engine
from app.models.models import Base, Product, Sale

Base.metadata.create_all(bind=engine)

days_back = 60
num_sales = 200

def populate_sales_data():
    db = SessionLocal()
    try:
        product_ids = [p.id for p in db.query(Product).all()]
        if not product_ids:
            print("No products found. Please populate products first.")
            return

        for _ in range(num_sales):
            prod_id = random.choice(product_ids)
            sale_date = datetime.date.today() - datetime.timedelta(days=random.randint(0, days_back))
            quantity = random.randint(1, 10)

            prod = db.query(Product).get(prod_id)
            total_amount = round(float(prod.unit_price) * quantity, 2)

            sale = Sale(
                product_id=prod_id,
                sale_date=sale_date,
                quantity=quantity,
                total_amount=total_amount,
                created_at=datetime.datetime.utcnow()
            )
            db.add(sale)

        db.commit()
        print(f"{num_sales} dummy sales records created from last {days_back} days.")
    finally:
        db.close()

if __name__ == '__main__':
    populate_sales_data()

