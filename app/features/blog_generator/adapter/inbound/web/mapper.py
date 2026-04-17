from __future__ import annotations

from app.features.blog_generator.adapter.inbound.web.dto.response import (
    BlogGenerateResponse,
    SEOMetaResponse,
)
from app.features.blog_generator.application.result.blog_result import BlogResult


class BlogWebMapper:
    """Maps application-layer results to web-layer response DTOs."""

    @staticmethod
    def to_response(result: BlogResult) -> BlogGenerateResponse:
        seo_data = result.seo or {}
        return BlogGenerateResponse(
            blog_id=result.blog_id,
            title=result.title,
            body=result.body,
            outline=result.outline,
            seo=SEOMetaResponse(
                meta_title=seo_data.get("meta_title", ""),
                meta_description=seo_data.get("meta_description", ""),
                slug=seo_data.get("slug", ""),
                focus_keyword=seo_data.get("focus_keyword", ""),
                secondary_keywords=seo_data.get("secondary_keywords", []),
                word_count=seo_data.get("word_count", 0),
                readability_score=seo_data.get("readability_score", 0.0),
                reading_time_minutes=seo_data.get("reading_time_minutes", 0),
            ),
            tokens_used=result.tokens_used,
            status=result.status,
        )

    @staticmethod
    def to_response_list(results: list[BlogResult]) -> list[BlogGenerateResponse]:
        return [BlogWebMapper.to_response(r) for r in results]
