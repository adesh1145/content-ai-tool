from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class AdCopyCreatedEvent(DomainEvent):
    """Raised when ad copy generation completes successfully."""

    platform: str = ""
    num_variations: int = 0
    tokens_used: int = 0
