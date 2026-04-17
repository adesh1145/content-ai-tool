from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.blog_generator.adapter.outbound.persistence.entity import BlogContentModel
from app.features.blog_generator.adapter.outbound.persistence.mapper import BlogPersistenceMapper
from app.features.blog_generator.domain.model.blog_content import BlogContent
from app.features.blog_generator.domain.port.outbound.blog_repository_port import IBlogRepository


class SQLAlchemyBlogRepository(IBlogRepository):
    """Driven adapter — persists BlogContent aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: BlogContent) -> BlogContent:
        existing = await self._session.get(BlogContentModel, entity.id)
        if existing:
            BlogPersistenceMapper.update_model(existing, entity)
        else:
            model = BlogPersistenceMapper.to_model(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> BlogContent | None:
        model = await self._session.get(BlogContentModel, id)
        return BlogPersistenceMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[BlogContent]:
        result = await self._session.execute(
            select(BlogContentModel)
            .order_by(BlogContentModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return [BlogPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(BlogContentModel, id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def list_by_user(
        self, user_id: str, *, limit: int = 20, offset: int = 0
    ) -> list[BlogContent]:
        result = await self._session.execute(
            select(BlogContentModel)
            .where(BlogContentModel.user_id == user_id)
            .order_by(BlogContentModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [BlogPersistenceMapper.to_domain(m) for m in result.scalars().all()]
