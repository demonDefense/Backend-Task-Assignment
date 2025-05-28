from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from app.crud.inventory_crud import *
from app.schemas.schemas import Inventory as InventorySchema, InventoryCreate, InventoryHistory as InventoryHistorySchema
from app.crud.product_crud import get_product
from app.api.endpoints.users import Isadmin

router = APIRouter(prefix="/inventory", tags=["Inventory"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[InventorySchema])
def read_inventory(db: Session = Depends(get_db)):
    return list_inventory(db)

@router.get("/low-stock", response_model=List[InventorySchema])
def read_low_stock(db: Session = Depends(get_db)):
    return list_low_stock(db)

@router.get("/{product_id}", response_model=InventorySchema)
def read_inventory_by_product(product_id: int, db: Session = Depends(get_db)):
    inv = get_inventory(db, product_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    return inv

@router.get("/history/", response_model=List[InventoryHistorySchema])
def read_inventory_history(db: Session = Depends(get_db)):
    return list_inventory_history(db)

@router.get("/history/{product_id}", response_model=List[InventoryHistorySchema])
def read_inventory_history_by_product(product_id: int, db: Session = Depends(get_db)):
    return get_inventory_history(db, product_id)

@router.post("/", response_model=InventorySchema, status_code=status.HTTP_201_CREATED)
def add_inventory(inv_in: InventoryCreate, db: Session = Depends(get_db)):
    product = get_product(db, inv_in.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    inv = get_inventory(db, inv_in.product_id)
    if inv:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inventory Already Exist, Try Update Request")
    return create_inventory(db, inv_in)
    
@router.put("/{product_id}", response_model=InventorySchema)
def adjust_inventory(product_id: int, change_qty: int, reason: str, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    inv = get_inventory(db, product_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    inv, hist = update_inventory(db, product_id, change_qty, reason)
    return inv

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_inventory(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    inv = get_inventory(db, product_id)
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory not found")
    success = delete_inventory(db, product_id)
    return success
    
