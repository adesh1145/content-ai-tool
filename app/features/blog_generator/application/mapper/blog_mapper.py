from __future__ import annotations

from app.features.blog_generator.application.result.blog_result import BlogResult
from app.features.blog_generator.domain.model.blog_content import BlogContent


class BlogMapper:
    """Maps domain aggregates to application-layer result DTOs."""

    @staticmethod
    def to_result(blog: BlogContent) -> BlogResult:
        return BlogResult(
            blog_id=blog.id,
            title=blog.title,
            body=blog.body,
            outline=list(blog.outline),
            seo={
                "meta_title": blog.seo.meta_title,
                "meta_description": blog.seo.meta_description,
                "slug": blog.seo.slug,
                "focus_keyword": blog.seo.focus_keyword,
                "secondary_keywords": list(blog.seo.secondary_keywords),
                "word_count": blog.seo.word_count,
                "readability_score": blog.seo.readability_score,
                "reading_time_minutes": blog.seo.reading_time_minutes,
            },
            tokens_used=blog.tokens_used,
            status=blog.status.value,
        )

    @staticmethod
    def to_result_list(blogs: list[BlogContent]) -> list[BlogResult]:
        return [BlogMapper.to_result(b) for b in blogs]
