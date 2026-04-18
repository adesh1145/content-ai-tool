"""Maps SEO application results → REST response DTOs."""

from __future__ import annotations

from app.features.seo_optimizer.application.result.meta_result import MetaResult
from app.features.seo_optimizer.application.result.seo_analysis_result import SEOAnalysisResult
from app.features.seo_optimizer.presentation.rest.dto.response import (
    KeywordAnalysisResponse,
    MetaGenerateResponse,
    SEOAnalyzeResponse,
)


class SEORestMapper:
    @staticmethod
    def analysis_to_response(result: SEOAnalysisResult) -> SEOAnalyzeResponse:
        return SEOAnalyzeResponse(
            analysis_id=result.analysis_id,
            overall_score=result.overall_score,
            readability_score=result.readability_score,
            flesch_reading_ease=result.flesch_reading_ease,
            flesch_kincaid_grade=result.flesch_kincaid_grade,
            avg_sentence_length=result.avg_sentence_length,
            word_count=result.word_count,
            heading_count=result.heading_count,
            has_h1=result.has_h1,
            internal_links_count=result.internal_links_count,
            external_links_count=result.external_links_count,
            image_count=result.image_count,
            images_with_alt=result.images_with_alt,
            has_meta_title=result.has_meta_title,
            has_meta_description=result.has_meta_description,
            meta_title_length=result.meta_title_length,
            meta_description_length=result.meta_description_length,
            keyword_analyses=[
                KeywordAnalysisResponse(
                    keyword=ka.keyword,
                    density_percent=ka.density_percent,
                    occurrences=ka.occurrences,
                    is_in_title=ka.is_in_title,
                    is_in_first_paragraph=ka.is_in_first_paragraph,
                    is_in_headings=ka.is_in_headings,
                    recommendation=ka.recommendation,
                )
                for ka in result.keyword_analyses
            ],
            recommendations=result.recommendations,
            tokens_used=result.tokens_used,
        )

    @staticmethod
    def meta_to_response(result: MetaResult) -> MetaGenerateResponse:
        return MetaGenerateResponse(
            meta_title=result.meta_title,
            meta_description=result.meta_description,
            slug=result.slug,
            tokens_used=result.tokens_used,
        )
