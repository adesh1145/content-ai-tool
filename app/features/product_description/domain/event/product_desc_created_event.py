from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ProductDescCreatedEvent(DomainEvent):
    """Raised when product description generation completes successfully."""

    product_name: str = ""
    word_count: int = 0
    tokens_used: int = 0
