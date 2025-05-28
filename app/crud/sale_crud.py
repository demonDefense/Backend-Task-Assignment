from sqlalchemy.orm import Session
from datetime import date
from typing import List, Tuple, Dict
from sqlalchemy import func
from app.models.models import Sale, Product, Category
from app.schemas.schemas import SaleCreate

def get_sale(db: Session, sale_id: int) -> Sale:
    return db.query(Sale).filter(Sale.id == sale_id).first()

def list_sales(db: Session) -> List[Tuple[str, str, int, float]]:
    return (
        db.query(
            Product.name.label("product_name"),
            Category.name.label("category_name"),
            func.sum(Sale.quantity).label("units_sold"),
            func.sum(Sale.total_amount).label("revenue")
        )
        .join(Product, Sale.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        group_by(
            Product.id, Product.name
        )
        .order_by(Product.name)
        .all()
    )

def create_sale(db: Session, sale_in: SaleCreate) -> Sale:
    data = sale_in.dict()
    data.pop("token", None)
    db_sale = Sale(**data)
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def revenue_by_period(db: Session, period: str, start_date: date, end_date: date) -> List[Tuple[str, float]]:
    """
    Returns list of (period_label, total_revenue).
    Example period_label: '2025-05-28' for day, '2025-W21' for week, '2025-05' for month, '2025' for year.
    """
    fld = None
    if period == "day":
        fld = func.date(Sale.sale_date)
    elif period == "week":
        fld = func.concat(func.year(Sale.sale_date), "-W", func.week(Sale.sale_date))
    elif period == "month":
        fld = func.date_format(Sale.sale_date, "%Y-%m")
    elif period == "year":
        fld = func.year(Sale.sale_date)
    else:
        raise ValueError("Invalid period")

    rows = (
        db.query(fld.label("period"), func.sum(Sale.total_amount).label("revenue"))
          .filter(Sale.sale_date.between(start_date, end_date))
          .group_by("period")
          .order_by("period")
          .all()
    )
    return rows 

def revenue_comparison(db: Session, start1: date, end1: date, start2: date, end2: date) -> Dict[str, float]:
    """
    Returns list of (period_label, total_revenue).
    Compare total revenue between two intervals.
    """
    rev1 = db.query(func.sum(Sale.total_amount)).filter(Sale.sale_date.between(start1, end1)).scalar() or 0
    rev2 = db.query(func.sum(Sale.total_amount)).filter(Sale.sale_date.between(start2, end2)).scalar() or 0
    return {"period1": float(rev1), "period2": float(rev2)}

def sales_by_period_category(db: Session, start_date: date, end_date: date) -> List[Tuple[str, int, float]]:
    """
    Returns list of (Category, items_sold, total_revenue).
    Compare total revenue between interval and categories
    """
    rows = (
        db.query(
            Category.name.label("category"),
            func.sum(Sale.quantity).label("units_sold"),
            func.sum(Sale.total_amount).label("revenue")
        )
        .join(Product, Product.id == Sale.product_id)
        .join(Category, Category.id == Product.category_id)
        .filter(Sale.sale_date.between(start_date, end_date))
        .group_by(Category.name)
        .all()
    )
    return rows

def get_sales_by_date_range(db: Session, start_date: date, end_date: date) -> List[Sale]:
    """
    Returns list of Sales.
    Give Sale data between date Range
    """
    return db.query(Sale).filter(Sale.sale_date.between(start_date, end_date)).order_by(Sale.sale_date).all()

def get_sales_by_product(db: Session, start_date: date, end_date: date, product_id: int) -> List[Tuple[str, str, int, float]]:
    """
    Returns list of (Product Category, items_sold, total_revenue).
    Calculate total revenue between interval and for specific Product
    """
    return (
        db.query(
            Product.name.label("product_name"),
            Category.name.label("category_name"),
            func.sum(Sale.quantity).label("units_sold"),
            func.sum(Sale.total_amount).label("total_revenue")
        )
        .join(Product, Sale.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .filter(Sale.sale_date.between(start_date, end_date))
        .filter(Product.id == product_id)
        .group_by(Product.id, Product.name)
        .order_by(Product.name)
        .all()
    )

def get_sales_by_category(db: Session, start_date: date, end_date: date, category_id: int) -> List[Tuple[str, int, float]]:
    """
    Returns list of (Category, items_sold, total_revenue).
    Calculate total revenue between interval and for specific Category
    """
    return (
        db.query(
            Category.name.label("category_name"),
            func.sum(Sale.quantity).label("units_sold"),
            func.sum(Sale.total_amount).label("total_revenue")
        )
        .join(Product, Sale.product_id == Product.id)
        .join(Category, Product.category_id == Category.id)
        .filter(Sale.sale_date.between(start_date, end_date))
        .filter(Category.id == category_id)
        .group_by(Category.id, Category.name)
        .order_by(Category.name)
        .all()
    )

