"""
Dependency container for the Email Writer v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.email_writer.domain.port.outbound.email_ai_port import EmailAIPort
from app.features.email_writer.domain.port.outbound.email_repository_port import EmailRepositoryPort
from app.features.email_writer.application.port.inbound.generate_email_port import GenerateEmailPort

from app.features.email_writer.infrastructure.ai.service import EmailAIService
from app.features.email_writer.infrastructure.messaging.publisher import EmailEventPublisher
from app.features.email_writer.infrastructure.persistence.repository import EmailRepositoryImpl
from app.features.email_writer.application.service.generate_email_service import GenerateEmailService


def get_email_repository(db: AsyncSession) -> EmailRepositoryPort:
    return EmailRepositoryImpl(db)


def get_email_ai_service() -> EmailAIPort:
    return EmailAIService()


def get_event_publisher() -> EventPublisherPort:
    return EmailEventPublisher()


def get_generate_email_service(db: AsyncSession) -> GenerateEmailPort:
    return GenerateEmailService(
        email_repo=get_email_repository(db),
        email_ai=get_email_ai_service(),
        event_publisher=get_event_publisher(),
    )
