from fastapi import FastAPI
from database import engine
from app.models.models import Base
from app.api.endpoints import products, sales, inventory, category, users

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce Admin API")

app.include_router(users.router)
app.include_router(category.router)
app.include_router(products.router)
#app.include_router(sales.router)
#app.include_router(inventory.router)

