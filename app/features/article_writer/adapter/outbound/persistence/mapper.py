from __future__ import annotations

from app.common.domain.value_objects import GenerationStatus, Language, Tone
from app.features.article_writer.adapter.outbound.persistence.entity import (
    ArticleContentModel,
)
from app.features.article_writer.domain.model.article import Article


class ArticleMapper:
    @staticmethod
    def to_domain(model: ArticleContentModel) -> Article:
        return Article(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_id=model.user_id,
            topic=model.topic,
            title=model.title or "",
            content=model.body or "",
            outline=model.outline_json or "",
            tone=Tone(model.tone),
            language=Language(model.language),
            target_audience=model.target_audience or "",
            word_count_target=model.word_count_target,
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used,
            error_message=model.error_message or "",
        )

    @staticmethod
    def to_orm(entity: Article) -> ArticleContentModel:
        return ArticleContentModel(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            user_id=entity.user_id,
            topic=entity.topic,
            title=entity.title or None,
            body=entity.content or None,
            outline_json=entity.outline or None,
            tone=entity.tone.value,
            language=entity.language.value,
            target_audience=entity.target_audience or None,
            word_count_target=entity.word_count_target,
            status=entity.status.value,
            tokens_used=entity.tokens_used,
            error_message=entity.error_message or None,
        )

    @staticmethod
    def update_orm(model: ArticleContentModel, entity: Article) -> None:
        model.user_id = entity.user_id
        model.topic = entity.topic
        model.title = entity.title or None
        model.body = entity.content or None
        model.outline_json = entity.outline or None
        model.tone = entity.tone.value
        model.language = entity.language.value
        model.target_audience = entity.target_audience or None
        model.word_count_target = entity.word_count_target
        model.status = entity.status.value
        model.tokens_used = entity.tokens_used
        model.error_message = entity.error_message or None
        model.updated_at = entity.updated_at
