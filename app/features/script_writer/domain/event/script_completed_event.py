from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ScriptCompletedEvent(DomainEvent):
    """Raised when script generation completes successfully."""

    script_format: str = ""
    topic: str = ""
    estimated_duration_seconds: int = 0
