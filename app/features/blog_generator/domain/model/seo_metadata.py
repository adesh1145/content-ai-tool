from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SEOMetadata:
    """Frozen value object holding SEO-related metadata for a blog post."""

    meta_title: str = ""
    meta_description: str = ""
    slug: str = ""
    focus_keyword: str = ""
    secondary_keywords: tuple[str, ...] = ()
    word_count: int = 0
    readability_score: float = 0.0
    reading_time_minutes: int = 0
