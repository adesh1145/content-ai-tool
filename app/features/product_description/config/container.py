"""
Dependency container for the Product Description v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.product_description.infrastructure.ai.service import ProductAIService
from app.features.product_description.infrastructure.messaging.publisher import ProductEventPublisher
from app.features.product_description.infrastructure.persistence.repository import ProductRepositoryImpl
from app.features.product_description.application.service.generate_product_service import GenerateProductService


def get_product_repository(db: AsyncSession) -> ProductRepositoryImpl:
    return ProductRepositoryImpl(db)


def get_product_ai_service() -> ProductAIService:
    return ProductAIService()


def get_event_publisher() -> ProductEventPublisher:
    return ProductEventPublisher()


def get_generate_product_service(db: AsyncSession) -> GenerateProductService:
    return GenerateProductService(
        product_repo=get_product_repository(db),
        product_ai=get_product_ai_service(),
        event_publisher=get_event_publisher(),
    )
