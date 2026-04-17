from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class UserLoggedInEvent(DomainEvent):
    """Raised when a user successfully authenticates."""

    aggregate_type: str = "User"
    email: str = ""
