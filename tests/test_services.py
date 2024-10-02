import pytest
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app import models, schemas
from app.services import OrderService


@pytest.mark.asyncio
async def test_create_order_success(mocker: MockerFixture):
    db = mocker.AsyncMock(AsyncSession)
    order_data = schemas.OrderCreate(
        items=[schemas.OrderItemCreate(product_id=1, quantity=2)]
    )
    product = models.Product(id=1, name="Test Product", stock=10,
                             is_deleted=False)

    mocker.patch("app.crud.products.get_product", return_value=product)
    mock_update_product = mocker.patch("app.crud.products.update_product")

    order = await OrderService.create_order(db, order_data)
    assert order.status == models.OrderStatus.processing
    assert mock_update_product.called


@pytest.mark.asyncio
async def test_create_order_product_not_available(mocker: MockerFixture):
    db = mocker.AsyncMock(AsyncSession)
    order_data = schemas.OrderCreate(
        items=[schemas.OrderItemCreate(product_id=1, quantity=2)]
    )
    product = models.Product(id=1, name="Test Product", stock=10,
                             is_deleted=True)

    mocker.patch("app.crud.products.get_product", return_value=product)

    with pytest.raises(HTTPException) as excinfo:
        await OrderService.create_order(db, order_data)
    assert excinfo.value.status_code == 400
    assert "не доступен для заказа" in excinfo.value.detail


@pytest.mark.asyncio
async def test_create_order_insufficient_stock(mocker: MockerFixture):
    db = mocker.AsyncMock(AsyncSession)
    order_data = schemas.OrderCreate(
        items=[schemas.OrderItemCreate(product_id=1, quantity=20)]
    )
    product = models.Product(id=1, name="Test Product", stock=10,
                             is_deleted=False)

    mocker.patch("app.crud.products.get_product", return_value=product)

    with pytest.raises(HTTPException) as excinfo:
        await OrderService.create_order(db, order_data)
    assert excinfo.value.status_code == 400
    assert "превышает остаток на складе" in excinfo.value.detail
