"""
Dependency container for the SEO Optimizer feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.seo_optimizer.adapter.outbound.ai.service import SEOAIService
from app.features.seo_optimizer.adapter.outbound.messaging.publisher import SEOEventPublisher
from app.features.seo_optimizer.adapter.outbound.persistence.repository import (
    SEORepositoryImpl,
)
from app.features.seo_optimizer.application.service.analyze_seo_service import (
    AnalyzeSEOService,
)
from app.features.seo_optimizer.application.service.generate_meta_service import (
    GenerateMetaService,
)


def get_seo_repository(db: AsyncSession) -> SEORepositoryImpl:
    return SEORepositoryImpl(db)


def get_seo_ai_service() -> SEOAIService:
    return SEOAIService()


def get_event_publisher() -> SEOEventPublisher:
    return SEOEventPublisher()


def get_analyze_seo_usecase(db: AsyncSession) -> AnalyzeSEOService:
    return AnalyzeSEOService(
        seo_repo=get_seo_repository(db),
        seo_ai=get_seo_ai_service(),
        event_publisher=get_event_publisher(),
    )


def get_generate_meta_usecase(db: AsyncSession) -> GenerateMetaService:
    return GenerateMetaService(
        seo_ai=get_seo_ai_service(),
    )
