from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Tuple, Optional
from app.models.models import Inventory, InventoryHistory
from app.schemas.schemas import InventoryCreate, InventoryHistoryCreate

def get_inventory(db: Session, product_id: int) -> Optional[Inventory]:
    return db.query(Inventory).filter(Inventory.product_id == product_id).first()


def list_inventory(db: Session) -> List[Inventory]:
    return db.query(Inventory).all()


def list_low_stock(db: Session) -> List[Inventory]:
    return db.query(Inventory).filter(Inventory.quantity_on_hand <= Inventory.low_stock_threshold).all()


def create_inventory(db: Session, inv_in: InventoryCreate) -> Inventory:
    inv = Inventory(
        product_id=inv_in.product_id,
        quantity_on_hand=inv_in.quantity_on_hand,
        low_stock_threshold=inv_in.low_stock_threshold,
        last_updated=datetime.utcnow()
    )
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv


def update_inventory(db: Session, product_id: int, change_qty: int, reason: str) -> Tuple[Optional[Inventory], Optional[InventoryHistory]]:
    inv = get_inventory(db, product_id)
    inv.quantity_on_hand += change_qty
    inv.last_updated = datetime.utcnow()
    hist = InventoryHistory(
        product_id=product_id,
        change_qty=change_qty,
        reason=reason,
        changed_at=datetime.utcnow()
    )
    db.add(inv)
    db.add(hist)
    db.commit()
    db.refresh(inv)
    db.refresh(hist)
    return inv, hist

def delete_inventory(db: Session, product_id: int) -> bool:
    inv = get_inventory(db, product_id)
    db.delete(inv)
    db.commit()
    return True

def list_inventory_history(db: Session) -> List[InventoryHistory]:
    return db.query(InventoryHistory).order_by(InventoryHistory.changed_at.desc()).all()

def get_inventory_history(db: Session, product_id: int) -> List[InventoryHistory]:
    return db.query(InventoryHistory).filter(Inventory.product_id == product_id).order_by(InventoryHistory.changed_at.desc()).all()
