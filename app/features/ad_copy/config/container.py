"""
Dependency container for the Ad Copy v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.ad_copy.adapter.outbound.ai.service import AdCopyAIService
from app.features.ad_copy.adapter.outbound.messaging.publisher import AdCopyEventPublisher
from app.features.ad_copy.adapter.outbound.persistence.repository import AdCopyRepositoryImpl
from app.features.ad_copy.application.service.generate_ad_service import GenerateAdService


def get_ad_repository(db: AsyncSession) -> AdCopyRepositoryImpl:
    return AdCopyRepositoryImpl(db)


def get_ad_ai_service() -> AdCopyAIService:
    return AdCopyAIService()


def get_event_publisher() -> AdCopyEventPublisher:
    return AdCopyEventPublisher()


def get_generate_ad_service(db: AsyncSession) -> GenerateAdService:
    return GenerateAdService(
        ad_repo=get_ad_repository(db),
        ad_ai=get_ad_ai_service(),
        event_publisher=get_event_publisher(),
    )
