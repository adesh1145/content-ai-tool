"""
Dependency container for the Article Writer v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle: use cases depend on abstractions
(ports) that are satisfied by concrete adapters assembled here.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.article_writer.domain.port.outbound.article_ai_port import IArticleAIService
from app.features.article_writer.domain.port.outbound.article_repository_port import IArticleRepository
from app.features.article_writer.application.port.inbound.generate_article_port import IGenerateArticlePort
from app.features.article_writer.application.port.inbound.get_article_port import IGetArticlePort

from app.features.article_writer.infrastructure.ai.service import (
    ArticleGraphService,
)
from app.features.article_writer.infrastructure.messaging.publisher import (
    ArticleEventPublisher,
)
from app.features.article_writer.infrastructure.persistence.repository import (
    ArticleRepositoryImpl,
)
from app.features.article_writer.application.service.generate_article_service import (
    GenerateArticleService,
)
from app.features.article_writer.application.service.get_article_service import (
    GetArticleService,
)


def get_article_repository(db: AsyncSession) -> IArticleRepository:
    return ArticleRepositoryImpl(db)


def get_article_ai_service() -> IArticleAIService:
    return ArticleGraphService()


def get_event_publisher() -> EventPublisherPort:
    return ArticleEventPublisher()


def get_generate_article_service(db: AsyncSession) -> IGenerateArticlePort:
    return GenerateArticleService(
        article_repo=get_article_repository(db),
        article_ai=get_article_ai_service(),
        event_publisher=get_event_publisher(),
    )


def get_get_article_service(db: AsyncSession) -> IGetArticlePort:
    return GetArticleService(article_repo=get_article_repository(db))
