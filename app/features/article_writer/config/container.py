"""
Dependency container for the Article Writer v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle: use cases depend on abstractions
(ports) that are satisfied by concrete adapters assembled here.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.article_writer.adapter.outbound.ai.service import (
    ArticleGraphService,
)
from app.features.article_writer.adapter.outbound.messaging.publisher import (
    ArticleEventPublisher,
)
from app.features.article_writer.adapter.outbound.persistence.repository import (
    ArticleRepositoryImpl,
)
from app.features.article_writer.application.service.generate_article_service import (
    GenerateArticleService,
)
from app.features.article_writer.application.service.get_article_service import (
    GetArticleService,
)


def get_article_repository(db: AsyncSession) -> ArticleRepositoryImpl:
    return ArticleRepositoryImpl(db)


def get_article_ai_service() -> ArticleGraphService:
    return ArticleGraphService()


def get_event_publisher() -> ArticleEventPublisher:
    return ArticleEventPublisher()


def get_generate_article_service(db: AsyncSession) -> GenerateArticleService:
    return GenerateArticleService(
        article_repo=get_article_repository(db),
        article_ai=get_article_ai_service(),
        event_publisher=get_event_publisher(),
    )


def get_get_article_service(db: AsyncSession) -> GetArticleService:
    return GetArticleService(article_repo=get_article_repository(db))
