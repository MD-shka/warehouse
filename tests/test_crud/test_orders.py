# test_crud/test_orders.py

import pytest
from pytest_mock import MockerFixture
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app import models
from app.crud.orders import update_order_status


@pytest.mark.asyncio
async def test_update_order_status_success(mocker: MockerFixture):
    db = mocker.AsyncMock(AsyncSession)
    order = models.Order(
        id=1,
        created_at=datetime.utcnow(),
        status=models.OrderStatus.delivered
    )
    mocker.patch("app.crud.orders.get_order", return_value=order)

    result = await update_order_status(db, 1, models.OrderStatus.delivered)
    assert result.status == models.OrderStatus.delivered


@pytest.mark.asyncio
async def test_update_order_status_order_not_found(mocker: MockerFixture):
    db = mocker.AsyncMock(AsyncSession)
    mocker.patch("app.crud.orders.get_order", return_value=None)

    with pytest.raises(HTTPException) as excinfo:
        await update_order_status(db, 1, models.OrderStatus.delivered)
    assert excinfo.value.status_code == 404
    assert "Заказ не найден" in excinfo.value.detail





