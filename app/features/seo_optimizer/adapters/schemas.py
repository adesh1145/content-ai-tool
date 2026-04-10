"""
app/features/seo_optimizer/adapters/schemas.py
"""

from __future__ import annotations
from pydantic import BaseModel, Field


class SEOAnalyzeRequest(BaseModel):
    content: str = Field(..., min_length=100, description="Content to analyze (markdown or plain text)")
    focus_keyword: str = Field("", max_length=100)
    meta_title: str = Field("", max_length=70)
    meta_description: str = Field("", max_length=200)
    url: str = Field("", max_length=500)


class KeywordAnalysisResponse(BaseModel):
    keyword: str
    density_percent: float
    occurrences: int
    is_in_title: bool
    is_in_first_paragraph: bool
    is_in_headings: bool
    recommendation: str


class SEOAnalysisResponse(BaseModel):
    analysis_id: str
    seo_score: float               # 0-100
    readability_score: float       # 0-100 (Flesch Reading Ease)
    flesch_kincaid_grade: float    # Grade level
    word_count: int
    heading_count: int
    has_h1: bool
    internal_links_count: int
    external_links_count: int
    image_count: int
    images_with_alt: int
    meta_title_length: int
    meta_description_length: int
    keyword_analyses: list[KeywordAnalysisResponse]
    recommendations: list[str]


class MetaGenerateRequest(BaseModel):
    content: str = Field(..., min_length=100)
    focus_keyword: str = Field("", max_length=100)


class MetaGenerateResponse(BaseModel):
    meta_title: str
    meta_description: str
    slug: str
