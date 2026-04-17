from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ArticleStartedEvent(DomainEvent):
    topic: str = ""
    user_id: str = ""
