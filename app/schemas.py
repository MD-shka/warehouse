from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .models import OrderStatus


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float = Field(
        ...,
        gt=0,
        description="Цена не может быть отрицательным числом"
    )
    stock: int = Field(
        ...,
        ge=0,
        description="Количество на складе не может быть отрицательным числом"
    )


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    is_deleted: bool

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(
        ...,
        gt=0,
        description="Количество товара должно быть больше 0"
    )


class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int = Field(
        ...,
        gt=0,
        description="Количество товара должно быть больше 0"
    )

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class Order(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[OrderItem]

    class Config:
        from_attributes = True
