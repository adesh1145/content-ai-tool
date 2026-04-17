from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class BlogCompletedEvent(DomainEvent):
    """Raised when blog generation completes successfully."""

    title: str = ""
    word_count: int = 0
    tokens_used: int = 0
    aggregate_type: str = "BlogContent"
