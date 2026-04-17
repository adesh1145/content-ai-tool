from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class EmailCreatedEvent(DomainEvent):
    """Raised when email content generation completes successfully."""

    email_type: str = ""
    tokens_used: int = 0
