"""
Dependency container for the Product Description v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.product_description.domain.port.outbound.product_ai_port import ProductAIPort
from app.features.product_description.domain.port.outbound.product_repository_port import ProductRepositoryPort
from app.features.product_description.application.port.inbound.generate_product_desc_port import GenerateProductDescPort

from app.features.product_description.infrastructure.ai.service import ProductAIService
from app.features.product_description.infrastructure.messaging.publisher import ProductEventPublisher
from app.features.product_description.infrastructure.persistence.repository import ProductRepositoryImpl
from app.features.product_description.application.service.generate_product_service import GenerateProductService


def get_product_repository(db: AsyncSession) -> ProductRepositoryPort:
    return ProductRepositoryImpl(db)


def get_product_ai_service() -> ProductAIPort:
    return ProductAIService()


def get_event_publisher() -> EventPublisherPort:
    return ProductEventPublisher()


def get_generate_product_service(db: AsyncSession) -> GenerateProductDescPort:
    return GenerateProductService(
        product_repo=get_product_repository(db),
        product_ai=get_product_ai_service(),
        event_publisher=get_event_publisher(),
    )
