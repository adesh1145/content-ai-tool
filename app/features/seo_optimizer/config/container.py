"""
Dependency container for the SEO Optimizer feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.seo_optimizer.domain.port.outbound.seo_ai_port import ISEOAIPort
from app.features.seo_optimizer.domain.port.outbound.seo_repository_port import ISEORepository
from app.features.seo_optimizer.application.port.inbound.analyze_seo_port import IAnalyzeSEO
from app.features.seo_optimizer.application.port.inbound.generate_meta_port import IGenerateMeta

from app.features.seo_optimizer.infrastructure.ai.service import SEOAIService
from app.features.seo_optimizer.infrastructure.messaging.publisher import SEOEventPublisher
from app.features.seo_optimizer.infrastructure.persistence.repository import (
    SEORepositoryImpl,
)
from app.features.seo_optimizer.application.service.analyze_seo_service import (
    AnalyzeSEOService,
)
from app.features.seo_optimizer.application.service.generate_meta_service import (
    GenerateMetaService,
)


def get_seo_repository(db: AsyncSession) -> ISEORepository:
    return SEORepositoryImpl(db)


def get_seo_ai_service() -> ISEOAIPort:
    return SEOAIService()


def get_event_publisher() -> EventPublisherPort:
    return SEOEventPublisher()


def get_analyze_seo_usecase(db: AsyncSession) -> IAnalyzeSEO:
    return AnalyzeSEOService(
        seo_repo=get_seo_repository(db),
        seo_ai=get_seo_ai_service(),
        event_publisher=get_event_publisher(),
    )


def get_generate_meta_usecase(db: AsyncSession) -> IGenerateMeta:
    return GenerateMetaService(
        seo_ai=get_seo_ai_service(),
    )
