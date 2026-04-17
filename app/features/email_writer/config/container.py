"""
Dependency container for the Email Writer v2 feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.email_writer.adapter.outbound.ai.service import EmailAIService
from app.features.email_writer.adapter.outbound.messaging.publisher import EmailEventPublisher
from app.features.email_writer.adapter.outbound.persistence.repository import EmailRepositoryImpl
from app.features.email_writer.application.service.generate_email_service import GenerateEmailService


def get_email_repository(db: AsyncSession) -> EmailRepositoryImpl:
    return EmailRepositoryImpl(db)


def get_email_ai_service() -> EmailAIService:
    return EmailAIService()


def get_event_publisher() -> EmailEventPublisher:
    return EmailEventPublisher()


def get_generate_email_service(db: AsyncSession) -> GenerateEmailService:
    return GenerateEmailService(
        email_repo=get_email_repository(db),
        email_ai=get_email_ai_service(),
        event_publisher=get_event_publisher(),
    )
