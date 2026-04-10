"""
app/features/seo_optimizer/entities/seo_analysis.py
─────────────────────────────────────────────────────────────
SEO Analysis domain entity.
Layer 1: Zero external dependencies.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from app.core.entities.base_entity import BaseEntity


@dataclass
class KeywordAnalysis:
    keyword: str = ""
    density_percent: float = 0.0
    occurrences: int = 0
    is_in_title: bool = False
    is_in_first_paragraph: bool = False
    is_in_headings: bool = False
    recommendation: str = ""


@dataclass
class SEOAnalysis(BaseEntity):
    user_id: str = ""
    content: str = ""
    url: str = ""

    # Readability
    flesch_reading_ease: float = 0.0         # 60-70 = good
    flesch_kincaid_grade: float = 0.0        # Grade level
    avg_sentence_length: float = 0.0

    # Keyword analysis
    focus_keyword: str = ""
    keyword_analyses: list[KeywordAnalysis] = field(default_factory=list)

    # On-page SEO
    word_count: int = 0
    has_meta_title: bool = False
    has_meta_description: bool = False
    meta_title_length: int = 0
    meta_description_length: int = 0
    heading_count: int = 0
    has_h1: bool = False
    internal_links_count: int = 0
    external_links_count: int = 0
    image_count: int = 0
    images_with_alt: int = 0

    # Scores
    seo_score: float = 0.0                   # 0-100
    readability_score: float = 0.0           # 0-100
    recommendations: list[str] = field(default_factory=list)
