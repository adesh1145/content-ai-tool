from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.article_writer.adapter.outbound.persistence.entity import (
    ArticleContentModel,
)
from app.features.article_writer.adapter.outbound.persistence.mapper import (
    ArticleMapper,
)
from app.features.article_writer.domain.model.article import Article
from app.features.article_writer.domain.port.outbound.article_repository_port import (
    IArticleRepository,
)


class ArticleRepositoryImpl(IArticleRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: Article) -> Article:
        existing = await self._session.get(ArticleContentModel, entity.id)
        if existing:
            ArticleMapper.update_orm(existing, entity)
            self._session.add(existing)
        else:
            model = ArticleMapper.to_orm(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> Article | None:
        model = await self._session.get(ArticleContentModel, id)
        return ArticleMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[Article]:
        stmt = select(ArticleContentModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [ArticleMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(ArticleContentModel, id)
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def get_by_user_id(
        self, user_id: str, *, skip: int = 0, limit: int = 50
    ) -> list[Article]:
        stmt = (
            select(ArticleContentModel)
            .where(ArticleContentModel.user_id == user_id)
            .order_by(ArticleContentModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [ArticleMapper.to_domain(m) for m in result.scalars().all()]
