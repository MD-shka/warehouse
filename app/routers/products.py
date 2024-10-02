# routers/products.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import schemas, database
from app.crud import products

router = APIRouter()


@router.post("/products/", response_model=schemas.Product)
async def create_product(
        product: schemas.ProductCreate,
        db: AsyncSession = Depends(database.get_db)
):
    return await products.create_product(db, product)


@router.get("/products/", response_model=list[schemas.Product])
async def get_products(db: AsyncSession = Depends(database.get_db)):
    return await products.get_products(db)


@router.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(
        product_id: int,
        db: AsyncSession = Depends(database.get_db)
):
    return await products.get_product(db, product_id)


@router.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(
        product_id: int,
        product: schemas.ProductCreate,
        db: AsyncSession = Depends(database.get_db)
):
    return await products.update_product(db, product_id, product)


@router.delete("/products/{product_id}")
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(database.get_db)
):
    return await products.delete_product(db, product_id)
