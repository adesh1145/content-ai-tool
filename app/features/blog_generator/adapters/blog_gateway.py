"""
app/features/blog_generator/adapters/blog_gateway.py
─────────────────────────────────────────────────────────────
IBlogRepository implementation using SQLAlchemy.
"""

from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.entities.value_objects import GenerationStatus, Language, Tone
from app.features.blog_generator.entities.blog_content import BlogContent, SEOMetadata
from app.features.blog_generator.use_cases.interfaces.blog_interfaces import IBlogRepository
from app.features.blog_generator.drivers.models import BlogContentModel


def _model_to_entity(m: BlogContentModel) -> BlogContent:
    seo_data = json.loads(m.seo_json or "{}")
    return BlogContent(
        id=m.id,
        user_id=m.user_id,
        project_id=m.project_id,
        topic=m.topic,
        title=m.title or "",
        outline=json.loads(m.outline_json or "[]"),
        body=m.body or "",
        tone=Tone(m.tone),
        language=Language(m.language),
        target_audience=m.target_audience or "",
        seo=SEOMetadata(
            meta_title=seo_data.get("meta_title", ""),
            meta_description=seo_data.get("meta_description", ""),
            slug=seo_data.get("slug", ""),
            focus_keyword=seo_data.get("focus_keyword", ""),
            secondary_keywords=seo_data.get("secondary_keywords", []),
            word_count=seo_data.get("word_count", 0),
            readability_score=seo_data.get("readability_score", 0.0),
            reading_time_minutes=seo_data.get("reading_time_minutes", 0),
        ),
        status=GenerationStatus(m.status),
        tokens_used=m.tokens_used or 0,
        error_message=m.error_message,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


class BlogGateway(IBlogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: BlogContent) -> BlogContent:
        existing = await self._session.get(BlogContentModel, entity.id)
        seo_json = json.dumps({
            "meta_title": entity.seo.meta_title,
            "meta_description": entity.seo.meta_description,
            "slug": entity.seo.slug,
            "focus_keyword": entity.seo.focus_keyword,
            "secondary_keywords": entity.seo.secondary_keywords,
            "word_count": entity.seo.word_count,
            "readability_score": entity.seo.readability_score,
            "reading_time_minutes": entity.seo.reading_time_minutes,
        })

        if existing:
            existing.title = entity.title
            existing.body = entity.body
            existing.outline_json = json.dumps(entity.outline)
            existing.seo_json = seo_json
            existing.status = entity.status.value
            existing.tokens_used = entity.tokens_used
            existing.error_message = entity.error_message
        else:
            model = BlogContentModel(
                id=entity.id,
                user_id=entity.user_id,
                project_id=entity.project_id,
                topic=entity.topic,
                title=entity.title,
                body=entity.body,
                outline_json=json.dumps(entity.outline),
                seo_json=seo_json,
                tone=entity.tone.value,
                language=entity.language.value,
                target_audience=entity.target_audience,
                status=entity.status.value,
                tokens_used=entity.tokens_used,
                error_message=entity.error_message,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
            self._session.add(model)

        await self._session.flush()
        return entity

    async def get_by_id(self, entity_id: str) -> BlogContent | None:
        model = await self._session.get(BlogContentModel, entity_id)
        return _model_to_entity(model) if model else None

    async def delete(self, entity_id: str) -> bool:
        model = await self._session.get(BlogContentModel, entity_id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def list_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> list[BlogContent]:
        result = await self._session.execute(
            select(BlogContentModel)
            .where(BlogContentModel.user_id == user_id)
            .order_by(BlogContentModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [_model_to_entity(m) for m in result.scalars().all()]
