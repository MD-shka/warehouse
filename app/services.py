from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from . import models
from .crud import products
from datetime import datetime


class OrderService:
    @staticmethod
    async def create_order(db: AsyncSession, order_data):
        for item in order_data.items:
            product = await products.get_product(db, item.product_id)
            if not product or product.is_deleted:
                raise HTTPException(
                    status_code=400,
                    detail=f"Товар с ID: {item.product_id}"
                           f" не доступен для заказа"
                )
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Количество товара: {product.name}"
                           f" превышает остаток на складе"
                )

        for item in order_data.items:
            product = await products.get_product(db, item.product_id)
            product.stock -= item.quantity
            await products.update_product(
                db,
                product.id,
                {'stock': product.stock}
            )

        order = models.Order(
            created_at=datetime.utcnow(),
            status=models.OrderStatus.processing
        )
        db.add(order)
        await db.commit()
        await db.refresh(order)
        await db.refresh(order, attribute_names=["items"])
        return order
