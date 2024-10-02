# routers/orders.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas, database
from app.crud import orders

router = APIRouter()


@router.post("/orders", response_model=schemas.OrderCreate, responses={
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "detail":
                        "Количество товара: Pepsi превышает остаток на складе"
                }
            }
        }
    },
    404: {
        "description": "Order not found",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Заказ не найден"
                }
            }
        }
    },
    500: {"description": "Internal Server Error"}
})
async def create_order(
        order: schemas.OrderCreate,
        db: AsyncSession = Depends(database.get_db)
):
    db_order = await orders.create_order(db, order)
    return schemas.Order.from_orm(db_order)


@router.get("/orders", response_model=list[schemas.Order])
async def get_orders(db: AsyncSession = Depends(database.get_db)):
    return await orders.get_orders(db)


@router.get("/orders/{order_id}", response_model=schemas.Order)
async def get_order(
        order_id: int,
        db: AsyncSession = Depends(database.get_db)
):
    return await orders.get_order(db, order_id)


@router.patch("/orders/{order_id}/status", response_model=schemas.Order)
async def update_order_status(
        order_id: int,
        new_status: models.OrderStatus,
        db: AsyncSession = Depends(database.get_db)
):
    return await orders.update_order_status(db, order_id, new_status)
