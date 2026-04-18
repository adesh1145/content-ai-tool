"""
Dependency container for the Social Media v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle: use cases depend on abstractions
(ports) that are satisfied by concrete adapters assembled here.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.social_media.infrastructure.ai.service import SocialAIService
from app.features.social_media.infrastructure.messaging.publisher import (
    SocialEventPublisher,
)
from app.features.social_media.infrastructure.persistence.repository import (
    SocialRepositoryImpl,
)
from app.features.social_media.application.service.generate_social_service import (
    GenerateSocialService,
)


def get_social_repository(db: AsyncSession) -> SocialRepositoryImpl:
    return SocialRepositoryImpl(db)


def get_social_ai_service() -> SocialAIService:
    return SocialAIService()


def get_event_publisher() -> SocialEventPublisher:
    return SocialEventPublisher()


def get_generate_social_service(db: AsyncSession) -> GenerateSocialService:
    return GenerateSocialService(
        social_repo=get_social_repository(db),
        social_ai=get_social_ai_service(),
        event_publisher=get_event_publisher(),
    )
