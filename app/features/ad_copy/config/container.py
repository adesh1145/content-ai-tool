"""
Dependency container for the Ad Copy v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.ad_copy.domain.port.outbound.ad_ai_port import AdAIPort
from app.features.ad_copy.domain.port.outbound.ad_repository_port import AdRepositoryPort
from app.features.ad_copy.application.port.inbound.generate_ad_port import GenerateAdPort

from app.features.ad_copy.infrastructure.ai.service import AdCopyAIService
from app.features.ad_copy.infrastructure.messaging.publisher import AdCopyEventPublisher
from app.features.ad_copy.infrastructure.persistence.repository import AdCopyRepositoryImpl
from app.features.ad_copy.application.service.generate_ad_service import GenerateAdService


def get_ad_repository(db: AsyncSession) -> AdRepositoryPort:
    return AdCopyRepositoryImpl(db)


def get_ad_ai_service() -> AdAIPort:
    return AdCopyAIService()


def get_event_publisher() -> EventPublisherPort:
    return AdCopyEventPublisher()


def get_generate_ad_service(db: AsyncSession) -> GenerateAdPort:
    return GenerateAdService(
        ad_repo=get_ad_repository(db),
        ad_ai=get_ad_ai_service(),
        event_publisher=get_event_publisher(),
    )
