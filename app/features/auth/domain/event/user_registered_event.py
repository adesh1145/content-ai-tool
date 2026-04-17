from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class UserRegisteredEvent(DomainEvent):
    """Raised when a new user account is successfully created."""

    aggregate_type: str = "User"
    email: str = ""
    full_name: str = ""
