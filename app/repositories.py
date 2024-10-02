from sqlalchemy.ext.asyncio import AsyncSession
from . import models
from sqlalchemy.future import select


class ProductRepository:
    @staticmethod
    async def create_product(db: AsyncSession, product: models.Product):
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def get_product(db: AsyncSession, product_id: int):
        result = await db.execute(
            select(models.Product).where(
                models.Product.id == product_id,
                models.Product.is_deleted == False
            )
        )
        return result.unique().scalar_one_or_none()

    @staticmethod
    async def get_products(db: AsyncSession):
        result = await db.execute(
            select(models.Product).where(models.Product.is_deleted == False)
        )
        return result.unique().scalars().all()

    async def update_product(
            self,
            db: AsyncSession,
            product_id: int,
            update_data
    ):
        product = await self.get_product(db, product_id)
        for key, value in update_data.items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product

    async def delete_product(self, db: AsyncSession, product_id: int):
        product = await self.get_product(db, product_id)
        if not product or product.is_deleted:
            return None
        product.is_deleted = True
        await db.commit()
        await db.refresh(product)
        return product
