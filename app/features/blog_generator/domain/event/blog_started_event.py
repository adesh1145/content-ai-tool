from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class BlogStartedEvent(DomainEvent):
    """Raised when a blog generation request begins processing."""

    user_id: str = ""
    topic: str = ""
    aggregate_type: str = "BlogContent"
