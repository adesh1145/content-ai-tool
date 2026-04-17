from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ArticleCompletedEvent(DomainEvent):
    topic: str = ""
    title: str = ""
    tokens_used: int = 0
    user_id: str = ""
