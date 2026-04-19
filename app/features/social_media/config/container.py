"""
Dependency container for the Social Media v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle: use cases depend on abstractions
(ports) that are satisfied by concrete adapters assembled here.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.social_media.domain.port.outbound.social_ai_port import ISocialAIService
from app.features.social_media.domain.port.outbound.social_repository_port import ISocialRepository
from app.features.social_media.application.port.inbound.generate_social_post_port import IGenerateSocialPostPort

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


def get_social_repository(db: AsyncSession) -> ISocialRepository:
    return SocialRepositoryImpl(db)

def get_social_ai_service() -> ISocialAIService:
    return SocialAIService()


def get_event_publisher() -> EventPublisherPort:
    return SocialEventPublisher()


def get_generate_social_service(db: AsyncSession) -> IGenerateSocialPostPort:
    return GenerateSocialService(
        social_repo=get_social_repository(db),
        social_ai=get_social_ai_service(),
        event_publisher=get_event_publisher(),
    )
