from __future__ import annotations

from dataclasses import dataclass, field

from app.features.seo_optimizer.domain.model.keyword_analysis import KeywordAnalysis


@dataclass
class SEOAnalysisResult:
    """Result returned by the analyze-SEO use case."""

    analysis_id: str = ""
    overall_score: float = 0.0
    readability_score: float = 0.0
    flesch_reading_ease: float = 0.0
    flesch_kincaid_grade: float = 0.0
    avg_sentence_length: float = 0.0
    word_count: int = 0
    heading_count: int = 0
    has_h1: bool = False
    internal_links_count: int = 0
    external_links_count: int = 0
    image_count: int = 0
    images_with_alt: int = 0
    has_meta_title: bool = False
    has_meta_description: bool = False
    meta_title_length: int = 0
    meta_description_length: int = 0
    keyword_analyses: list[KeywordAnalysis] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    tokens_used: int = 0
