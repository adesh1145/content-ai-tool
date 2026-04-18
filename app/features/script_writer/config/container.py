"""
Dependency container for the Script Writer feature.

Wires together domain, application, and adapter layers following
the Dependency Inversion Principle.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.script_writer.infrastructure.ai.service import ScriptAIService
from app.features.script_writer.infrastructure.messaging.publisher import (
    ScriptEventPublisher,
)
from app.features.script_writer.infrastructure.persistence.repository import (
    ScriptRepositoryImpl,
)
from app.features.script_writer.application.service.generate_script_service import (
    GenerateScriptService,
)


def get_script_repository(db: AsyncSession) -> ScriptRepositoryImpl:
    return ScriptRepositoryImpl(db)


def get_script_ai_service() -> ScriptAIService:
    return ScriptAIService()


def get_event_publisher() -> ScriptEventPublisher:
    return ScriptEventPublisher()


def get_generate_script_usecase(db: AsyncSession) -> GenerateScriptService:
    return GenerateScriptService(
        script_repo=get_script_repository(db),
        script_ai=get_script_ai_service(),
        event_publisher=get_event_publisher(),
    )
