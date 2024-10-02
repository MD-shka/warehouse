# crud/products.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app import models, schemas


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    try:
        db_product = models.Product(**product.dict())
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка создания продукта: {str(e)}"
        )


async def get_product(db: AsyncSession, product_id: int):
    try:
        result = await db.execute(
            select(models.Product).where(
                models.Product.id == product_id,
                models.Product.is_deleted == False
            )
        )
        product = result.unique().scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Продукт не найден"
            )
        return product
    except SQLAlchemyError as e:
        HTTPException(
            status_code=500,
            detail=f"Ошибка получения продукта: {str(e)}"
        )


async def get_products(db: AsyncSession):
    try:
        result = await db.execute(
            select(models.Product).where(models.Product.is_deleted == False)
        )
        return result.unique().scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения продуктов: {str(e)}"
        )


async def update_product(
        db: AsyncSession,
        product_id: int,
        update_data: schemas.ProductCreate
):
    try:
        product = await get_product(db, product_id)
        if not product:
            return None
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обновления продукта: {str(e)}"
        )


async def delete_product(db: AsyncSession, product_id: int):
    try:
        product = await get_product(db, product_id)
        if not product or product.is_deleted:
            return None
        product.is_deleted = True
        await db.commit()
        await db.refresh(product)
        return product
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка удаления продукта: {str(e)}"
        )
