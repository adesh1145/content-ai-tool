from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class SocialPostCreatedEvent(DomainEvent):
    platform: str = ""
    topic: str = ""
    char_count: int = 0
    user_id: str = ""
