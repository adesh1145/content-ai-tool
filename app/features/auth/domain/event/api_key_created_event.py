from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class APIKeyCreatedEvent(DomainEvent):
    """Raised when an API key is created for a user."""

    aggregate_type: str = "User"
    key_name: str = ""
    key_prefix: str = ""
