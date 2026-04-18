from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.social_media.infrastructure.persistence.entity import (
    SocialPostModel,
)
from app.features.social_media.infrastructure.persistence.mapper import (
    SocialPostMapper,
)
from app.features.social_media.domain.model.social_post import SocialPost
from app.features.social_media.domain.port.outbound.social_repository_port import (
    ISocialRepository,
)


class SocialRepositoryImpl(ISocialRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: SocialPost) -> SocialPost:
        existing = await self._session.get(SocialPostModel, entity.id)
        if existing:
            SocialPostMapper.update_orm(existing, entity)
            self._session.add(existing)
        else:
            model = SocialPostMapper.to_orm(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> SocialPost | None:
        model = await self._session.get(SocialPostModel, id)
        return SocialPostMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[SocialPost]:
        stmt = select(SocialPostModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [SocialPostMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(SocialPostModel, id)
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def get_by_user_id(
        self, user_id: str, *, skip: int = 0, limit: int = 50
    ) -> list[SocialPost]:
        stmt = (
            select(SocialPostModel)
            .where(SocialPostModel.user_id == user_id)
            .order_by(SocialPostModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [SocialPostMapper.to_domain(m) for m in result.scalars().all()]
