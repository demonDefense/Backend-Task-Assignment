from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import List, Optional, ForwardRef

# --- User & Role ---

class LoginRequest(BaseModel):
    username: str
    password: str

class RoleBase(BaseModel):
    name: str
    description: Optional[str]

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    token: str

class User(UserBase):
    id: int
    created_at: datetime
    last_login: Optional[datetime]
    roles: List[Role] = []

    class Config:
        orm_mode = True
        
class UserRoleBase(BaseModel):
    user_id: int
    role_id: int
    assigned_at: datetime

    class Config:
        orm_mode = True


# --- Category & Product ---

class CategoryBase(BaseModel):
    name: str
    description: Optional[str]

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    category_id: int
    unit_price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Category

    class Config:
        orm_mode = True


# --- Sales & Revenue ---

class SaleBase(BaseModel):
    product_id: int
    sale_date: date
    quantity: int
    total_amount: float

class SaleCreate(SaleBase):
    token: str

class Sale(SaleBase):
    id: int
    created_at: datetime
    product: Product

    class Config:
        orm_mode = True
        
class RevenueByPeriod(BaseModel):
    period: str
    revenue: float

    class Config:
        orm_mode = True
        
class RevenueByCategory(BaseModel):
    category: str
    units_sold: int
    revenue: float

    class Config:
        orm_mode = True
        
class RevenueByProduct(BaseModel):
    product: str
    category: str
    units_sold: int
    revenue: float

    class Config:
        orm_mode = True


# --- Inventory & History ---

class InventoryBase(BaseModel):
    product_id: int
    quantity_on_hand: int
    low_stock_threshold: Optional[int] = 10

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    last_updated: datetime
    product: Product

    class Config:
        orm_mode = True

class InventoryHistoryBase(BaseModel):
    product_id: int
    change_qty: int
    reason: Optional[str]

class InventoryHistoryCreate(InventoryHistoryBase):
    pass

class InventoryHistory(InventoryHistoryBase):
    id: int
    changed_at: datetime
    product: Product

    class Config:
        orm_mode = True

