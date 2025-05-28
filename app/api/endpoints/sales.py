from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Dict
from database import SessionLocal
from app.crud.sale_crud import *
from app.crud.product_crud import get_product
from app.schemas.schemas import SaleCreate, Sale, RevenueByCategory, RevenueByPeriod, RevenueByProduct
from app.api.endpoints.users import Isadmin

router = APIRouter(prefix="/sales", tags=["Sales"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Sale, status_code=status.HTTP_201_CREATED)
def create_new_sale(sale_in: SaleCreate, db: Session = Depends(get_db)):
    if Isadmin(sale_in.token, db):
        product = get_product(db, sale_in.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return create_sale(db, sale_in)

@router.get("/", response_model=List[RevenueByProduct])
def read_sales(db: Session = Depends(get_db)):
    rows = list_sales(db)
    return [RevenueByProduct(product=pro, category=cat, units_sold=int(units),revenue=float(rev)) for pro, cat, units, rev in rows]
    

@router.get("/{sale_id}", response_model=Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = get_sale(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.get("/revenue/", response_model=List[RevenueByPeriod], summary="Revenue by period")
def get_revenue(period: str = Query(..., description="one of day, week, month, year"), start: date = Query(...), end: date = Query(...),db: Session = Depends(get_db)):
    try:
        data = revenue_by_period(db, period, start, end)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid period")
    return [RevenueByPeriod(period= str(p), revenue= float(r)) for p, r in data]

@router.get("/revenue/compare", response_model=Dict[str, float], summary="Compare revenue periods")
def compare_revenue(start1: date = Query(...), end1: date = Query(...), start2: date = Query(...), end2: date = Query(...), db: Session = Depends(get_db)):
    return revenue_comparison(db, start1, end1, start2, end2)

@router.get("/revenue/category", response_model=List[RevenueByCategory], summary="Revenue by period and category")
def revenue_by_period_and_category(start: date = Query(...), end: date = Query(...), db: Session = Depends(get_db)):
    rows = sales_by_period_category(db, start, end)
    return [RevenueByCategory(category=cat, units_sold=int(units),revenue=float(rev)) for cat, units, rev in rows]

@router.get("/range/", response_model=List[Sale], summary="Sales in date range")
def sales_in_range(start: date = Query(...), end: date = Query(...), db: Session = Depends(get_db)):
    return get_sales_by_date_range(db, start, end)

@router.get("/product/", response_model=List[RevenueByProduct], summary="Sales in specific Product")
def sales_in_product(product_id: int, start: date = Query(...), end: date = Query(...), db: Session = Depends(get_db)):
    rows = get_sales_by_product(db, start, end, product_id)
    return [RevenueByProduct(product=pro, category=cat, units_sold=int(units),revenue=float(rev)) for pro, cat, units, rev in rows]
    
@router.get("/category/", response_model=List[RevenueByCategory], summary="Sales in specific Category")
def sales_in_category(category_id: int, start: date = Query(...), end: date = Query(...), db: Session = Depends(get_db)):
    rows = get_sales_by_category(db, start, end, category_id)
    return [RevenueByCategory(category=cat, units_sold=int(units),revenue=float(rev)) for cat, units, rev in rows]

