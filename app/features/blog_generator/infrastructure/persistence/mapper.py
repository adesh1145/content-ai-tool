from __future__ import annotations

import json

from app.common.domain.value_objects import GenerationStatus, Language, Tone
from app.features.blog_generator.domain.model.blog_content import BlogContent
from app.features.blog_generator.domain.model.seo_metadata import SEOMetadata
from app.features.blog_generator.infrastructure.persistence.entity import BlogContentModel


class BlogPersistenceMapper:
    """Bidirectional mapping between BlogContent aggregate and SQLAlchemy model."""

    @staticmethod
    def to_domain(model: BlogContentModel) -> BlogContent:
        seo_data: dict = json.loads(model.seo_json or "{}")
        return BlogContent(
            id=model.id,
            user_id=model.user_id,
            project_id=model.project_id,
            topic=model.topic,
            title=model.title or "",
            body=model.body or "",
            outline=json.loads(model.outline_json or "[]"),
            seo=SEOMetadata(
                meta_title=seo_data.get("meta_title", ""),
                meta_description=seo_data.get("meta_description", ""),
                slug=seo_data.get("slug", ""),
                focus_keyword=seo_data.get("focus_keyword", ""),
                secondary_keywords=tuple(seo_data.get("secondary_keywords", [])),
                word_count=seo_data.get("word_count", 0),
                readability_score=seo_data.get("readability_score", 0.0),
                reading_time_minutes=seo_data.get("reading_time_minutes", 0),
            ),
            tone=Tone(model.tone),
            language=Language(model.language),
            target_audience=model.target_audience or "",
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used or 0,
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: BlogContent) -> BlogContentModel:
        return BlogContentModel(
            id=entity.id,
            user_id=entity.user_id,
            project_id=entity.project_id,
            topic=entity.topic,
            title=entity.title,
            body=entity.body,
            outline_json=json.dumps(entity.outline),
            seo_json=json.dumps({
                "meta_title": entity.seo.meta_title,
                "meta_description": entity.seo.meta_description,
                "slug": entity.seo.slug,
                "focus_keyword": entity.seo.focus_keyword,
                "secondary_keywords": list(entity.seo.secondary_keywords),
                "word_count": entity.seo.word_count,
                "readability_score": entity.seo.readability_score,
                "reading_time_minutes": entity.seo.reading_time_minutes,
            }),
            tone=entity.tone.value if isinstance(entity.tone, Tone) else entity.tone,
            language=entity.language.value if isinstance(entity.language, Language) else entity.language,
            target_audience=entity.target_audience,
            status=entity.status.value if isinstance(entity.status, GenerationStatus) else entity.status,
            tokens_used=entity.tokens_used,
            error_message=entity.error_message,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: BlogContentModel, entity: BlogContent) -> None:
        model.title = entity.title
        model.body = entity.body
        model.outline_json = json.dumps(entity.outline)
        model.seo_json = json.dumps({
            "meta_title": entity.seo.meta_title,
            "meta_description": entity.seo.meta_description,
            "slug": entity.seo.slug,
            "focus_keyword": entity.seo.focus_keyword,
            "secondary_keywords": list(entity.seo.secondary_keywords),
            "word_count": entity.seo.word_count,
            "readability_score": entity.seo.readability_score,
            "reading_time_minutes": entity.seo.reading_time_minutes,
        })
        model.status = entity.status.value if isinstance(entity.status, GenerationStatus) else entity.status
        model.tokens_used = entity.tokens_used
        model.error_message = entity.error_message
