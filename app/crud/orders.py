# crud/orders.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from app import models, schemas
from app.services import OrderService


async def create_order(db: AsyncSession, order_data: schemas.OrderCreate):
    try:
        order_service = OrderService()
        db_order = await order_service.create_order(db, order_data)

        for item_data in order_data.items:
            order_item = models.OrderItem(
                order_id=db_order.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity
            )
            db.add(order_item)
        await db.commit()
        await db.refresh(db_order)
        await db.refresh(db_order, attribute_names=["items"])
        return schemas.Order.from_orm(db_order)
    except (SQLAlchemyError, ValueError) as e:
        await db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка создания заказа: {str(e)}"
        )


async def get_order(db: AsyncSession, order_id: int):
    try:
        result = await db.execute(
            select(models.Order)
            .options(joinedload(models.Order.items))
            .filter(models.Order.id == order_id)
        )
        order = result.unique().scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        return order
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка базы данных: {str(e)}"
        )


async def get_orders(db: AsyncSession):
    try:
        result = await db.execute(
            select(models.Order).options(joinedload(models.Order.items))
        )
        return result.unique().scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении заказов: {str(e)}"
        )


async def update_order_status(
        db: AsyncSession,
        order_id: int,
        new_status: models.OrderStatus
):
    try:
        order = await get_order(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        order.status = new_status
        await db.commit()
        await db.refresh(order)
        return schemas.Order.from_orm(order)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обновлении статуса заказа: {str(e)}"
        )
