from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.ad_copy.adapter.outbound.persistence.entity import AdCopyModel
from app.features.ad_copy.adapter.outbound.persistence.mapper import AdCopyMapper
from app.features.ad_copy.domain.model.ad_copy import AdCopy
from app.features.ad_copy.domain.port.outbound.ad_repository_port import AdRepositoryPort


class AdCopyRepositoryImpl(AdRepositoryPort):
    """Driven adapter — persists AdCopy aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: AdCopy) -> AdCopy:
        existing = await self._session.get(AdCopyModel, entity.id)
        if existing:
            AdCopyMapper.update_model(existing, entity)
        else:
            model = AdCopyMapper.to_model(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> AdCopy | None:
        model = await self._session.get(AdCopyModel, id)
        return AdCopyMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[AdCopy]:
        result = await self._session.execute(
            select(AdCopyModel).offset(skip).limit(limit)
        )
        return [AdCopyMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(AdCopyModel, id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def find_by_user_id(self, user_id: str) -> list[AdCopy]:
        result = await self._session.execute(
            select(AdCopyModel)
            .where(AdCopyModel.user_id == user_id)
            .order_by(AdCopyModel.created_at.desc())
        )
        return [AdCopyMapper.to_domain(m) for m in result.scalars().all()]
