from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class SEOAnalysisCompletedEvent(DomainEvent):
    """Raised when SEO analysis completes successfully."""

    overall_score: float = 0.0
    word_count: int = 0
    focus_keyword: str = ""
