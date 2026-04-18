from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.product_description.infrastructure.persistence.entity import ProductDescriptionModel
from app.features.product_description.infrastructure.persistence.mapper import ProductDescriptionMapper
from app.features.product_description.domain.model.product_description import ProductDescription
from app.features.product_description.domain.port.outbound.product_repository_port import ProductRepositoryPort


class ProductRepositoryImpl(ProductRepositoryPort):
    """Driven adapter — persists ProductDescription aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: ProductDescription) -> ProductDescription:
        existing = await self._session.get(ProductDescriptionModel, entity.id)
        if existing:
            ProductDescriptionMapper.update_model(existing, entity)
        else:
            model = ProductDescriptionMapper.to_model(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> ProductDescription | None:
        model = await self._session.get(ProductDescriptionModel, id)
        return ProductDescriptionMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[ProductDescription]:
        result = await self._session.execute(
            select(ProductDescriptionModel).offset(skip).limit(limit)
        )
        return [ProductDescriptionMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(ProductDescriptionModel, id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def find_by_user_id(self, user_id: str) -> list[ProductDescription]:
        result = await self._session.execute(
            select(ProductDescriptionModel)
            .where(ProductDescriptionModel.user_id == user_id)
            .order_by(ProductDescriptionModel.created_at.desc())
        )
        return [ProductDescriptionMapper.to_domain(m) for m in result.scalars().all()]
