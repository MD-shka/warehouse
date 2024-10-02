from fastapi import FastAPI
from app.routers import products, orders

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])
