from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.seo_optimizer.infrastructure.persistence.entity import SEOAnalysisModel
from app.features.seo_optimizer.infrastructure.persistence.mapper import SEOORMMapper
from app.features.seo_optimizer.domain.model.seo_analysis import SEOAnalysis
from app.features.seo_optimizer.domain.port.outbound.seo_repository_port import ISEORepository


class SEORepositoryImpl(ISEORepository):
    """Driven adapter — persists SEOAnalysis aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: SEOAnalysis) -> SEOAnalysis:
        existing = await self._session.get(SEOAnalysisModel, entity.id)
        if existing:
            SEOORMMapper.update_model(existing, entity)
        else:
            model = SEOORMMapper.to_model(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> SEOAnalysis | None:
        model = await self._session.get(SEOAnalysisModel, id)
        return SEOORMMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[SEOAnalysis]:
        result = await self._session.execute(
            select(SEOAnalysisModel)
            .offset(skip)
            .limit(limit)
            .order_by(SEOAnalysisModel.created_at.desc())
        )
        return [SEOORMMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(SEOAnalysisModel, id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def find_by_user_id(self, user_id: str) -> list[SEOAnalysis]:
        result = await self._session.execute(
            select(SEOAnalysisModel)
            .where(SEOAnalysisModel.user_id == user_id)
            .order_by(SEOAnalysisModel.created_at.desc())
        )
        return [SEOORMMapper.to_domain(m) for m in result.scalars().all()]
