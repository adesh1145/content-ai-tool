from __future__ import annotations

import json

from app.common.domain.value_objects import GenerationStatus
from app.features.seo_optimizer.infrastructure.persistence.entity import SEOAnalysisModel
from app.features.seo_optimizer.domain.model.seo_analysis import SEOAnalysis


class SEOORMMapper:
    """Bidirectional mapping between the SEOAnalysis aggregate and the SQLAlchemy model."""

    @staticmethod
    def to_domain(model: SEOAnalysisModel) -> SEOAnalysis:
        recommendations: list[str] = []
        if model.suggestions_json:
            try:
                recommendations = json.loads(model.suggestions_json)
            except (json.JSONDecodeError, TypeError):
                pass

        return SEOAnalysis(
            id=model.id,
            user_id=model.user_id,
            content_text=model.content_text or "",
            url=model.url,
            focus_keyword=model.focus_keyword,
            overall_score=model.overall_score,
            readability_score=model.readability_score,
            flesch_reading_ease=model.flesch_reading_ease,
            flesch_kincaid_grade=model.flesch_kincaid_grade,
            avg_sentence_length=model.avg_sentence_length,
            word_count=model.word_count,
            heading_count=model.heading_count,
            has_h1=model.has_h1,
            internal_links_count=model.internal_links_count,
            external_links_count=model.external_links_count,
            image_count=model.image_count,
            images_with_alt=model.images_with_alt,
            has_meta_title=model.has_meta_title,
            has_meta_description=model.has_meta_description,
            meta_title_length=model.meta_title_length,
            meta_description_length=model.meta_description_length,
            keyword_density_json=model.keyword_density_json or "",
            suggestions_json=model.suggestions_json or "",
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used,
            recommendations=recommendations,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: SEOAnalysis) -> SEOAnalysisModel:
        return SEOAnalysisModel(
            id=entity.id,
            user_id=entity.user_id,
            content_text=entity.content_text,
            url=entity.url,
            focus_keyword=entity.focus_keyword,
            overall_score=entity.overall_score,
            readability_score=entity.readability_score,
            flesch_reading_ease=entity.flesch_reading_ease,
            flesch_kincaid_grade=entity.flesch_kincaid_grade,
            avg_sentence_length=entity.avg_sentence_length,
            word_count=entity.word_count,
            heading_count=entity.heading_count,
            has_h1=entity.has_h1,
            internal_links_count=entity.internal_links_count,
            external_links_count=entity.external_links_count,
            image_count=entity.image_count,
            images_with_alt=entity.images_with_alt,
            has_meta_title=entity.has_meta_title,
            has_meta_description=entity.has_meta_description,
            meta_title_length=entity.meta_title_length,
            meta_description_length=entity.meta_description_length,
            keyword_density_json=entity.keyword_density_json,
            suggestions_json=entity.suggestions_json,
            status=entity.status.value,
            tokens_used=entity.tokens_used,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: SEOAnalysisModel, entity: SEOAnalysis) -> None:
        model.content_text = entity.content_text
        model.url = entity.url
        model.focus_keyword = entity.focus_keyword
        model.overall_score = entity.overall_score
        model.readability_score = entity.readability_score
        model.flesch_reading_ease = entity.flesch_reading_ease
        model.flesch_kincaid_grade = entity.flesch_kincaid_grade
        model.avg_sentence_length = entity.avg_sentence_length
        model.word_count = entity.word_count
        model.heading_count = entity.heading_count
        model.has_h1 = entity.has_h1
        model.internal_links_count = entity.internal_links_count
        model.external_links_count = entity.external_links_count
        model.image_count = entity.image_count
        model.images_with_alt = entity.images_with_alt
        model.has_meta_title = entity.has_meta_title
        model.has_meta_description = entity.has_meta_description
        model.meta_title_length = entity.meta_title_length
        model.meta_description_length = entity.meta_description_length
        model.keyword_density_json = entity.keyword_density_json
        model.suggestions_json = entity.suggestions_json
        model.status = entity.status.value
        model.tokens_used = entity.tokens_used
