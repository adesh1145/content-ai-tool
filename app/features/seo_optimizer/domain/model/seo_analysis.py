from __future__ import annotations

from dataclasses import dataclass, field

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import GenerationStatus
from app.features.seo_optimizer.domain.event.seo_analysis_completed_event import (
    SEOAnalysisCompletedEvent,
)
from app.features.seo_optimizer.domain.model.keyword_analysis import KeywordAnalysis


@dataclass
class SEOAnalysis(AggregateRoot):
    """SEO Analysis aggregate root — owns the lifecycle of an SEO analysis request."""

    user_id: str = ""
    content_text: str = ""
    url: str = ""
    focus_keyword: str = ""

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

    keyword_density_json: str = ""
    suggestions_json: str = ""

    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0

    _keyword_analyses: list[KeywordAnalysis] = field(default_factory=list, repr=False)
    recommendations: list[str] = field(default_factory=list)

    def complete_analysis(
        self,
        *,
        overall_score: float,
        readability_score: float,
        flesch_reading_ease: float,
        flesch_kincaid_grade: float,
        avg_sentence_length: float,
        word_count: int,
        heading_count: int,
        has_h1: bool,
        internal_links_count: int,
        external_links_count: int,
        image_count: int,
        images_with_alt: int,
        has_meta_title: bool,
        has_meta_description: bool,
        meta_title_length: int,
        meta_description_length: int,
        keyword_density_json: str,
        suggestions_json: str,
        recommendations: list[str],
        tokens_used: int,
    ) -> None:
        self.overall_score = overall_score
        self.readability_score = readability_score
        self.flesch_reading_ease = flesch_reading_ease
        self.flesch_kincaid_grade = flesch_kincaid_grade
        self.avg_sentence_length = avg_sentence_length
        self.word_count = word_count
        self.heading_count = heading_count
        self.has_h1 = has_h1
        self.internal_links_count = internal_links_count
        self.external_links_count = external_links_count
        self.image_count = image_count
        self.images_with_alt = images_with_alt
        self.has_meta_title = has_meta_title
        self.has_meta_description = has_meta_description
        self.meta_title_length = meta_title_length
        self.meta_description_length = meta_description_length
        self.keyword_density_json = keyword_density_json
        self.suggestions_json = suggestions_json
        self.recommendations = recommendations
        self.tokens_used = tokens_used
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            SEOAnalysisCompletedEvent(
                aggregate_id=self.id,
                aggregate_type="SEOAnalysis",
                overall_score=overall_score,
                word_count=word_count,
                focus_keyword=self.focus_keyword,
            )
        )

    def add_keyword_analysis(self, ka: KeywordAnalysis) -> None:
        self._keyword_analyses.append(ka)

    @property
    def keyword_analyses(self) -> list[KeywordAnalysis]:
        return list(self._keyword_analyses)

    def fail_analysis(self, error: str) -> None:
        self.suggestions_json = error
        self.status = GenerationStatus.FAILED
        self.touch()
