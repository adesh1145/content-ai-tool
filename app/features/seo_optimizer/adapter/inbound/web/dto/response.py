from __future__ import annotations

from pydantic import BaseModel, Field


class KeywordAnalysisResponse(BaseModel):
    """Single keyword analysis in the response."""

    keyword: str
    density_percent: float
    occurrences: int
    is_in_title: bool
    is_in_first_paragraph: bool
    is_in_headings: bool
    recommendation: str


class SEOAnalyzeResponse(BaseModel):
    """Outgoing response schema for SEO analysis."""

    analysis_id: str
    overall_score: float
    readability_score: float
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    avg_sentence_length: float
    word_count: int
    heading_count: int
    has_h1: bool
    internal_links_count: int
    external_links_count: int
    image_count: int
    images_with_alt: int
    has_meta_title: bool
    has_meta_description: bool
    meta_title_length: int
    meta_description_length: int
    keyword_analyses: list[KeywordAnalysisResponse] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    tokens_used: int


class MetaGenerateResponse(BaseModel):
    """Outgoing response schema for meta tag generation."""

    meta_title: str
    meta_description: str
    slug: str
    tokens_used: int
