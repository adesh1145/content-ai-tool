from __future__ import annotations

from app.common.domain.value_objects import GenerationStatus, Language, SocialPlatform, Tone
from app.features.social_media.adapter.outbound.persistence.entity import (
    SocialPostModel,
)
from app.features.social_media.domain.model.social_post import SocialPost


class SocialPostMapper:
    @staticmethod
    def to_domain(model: SocialPostModel) -> SocialPost:
        return SocialPost(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_id=model.user_id,
            platform=SocialPlatform(model.platform),
            topic=model.topic,
            content=model.content or "",
            hashtags=model.hashtags or [],
            tone=Tone(model.tone),
            language=Language(model.language),
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used,
            error_message=model.error_message or "",
        )

    @staticmethod
    def to_orm(entity: SocialPost) -> SocialPostModel:
        return SocialPostModel(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            user_id=entity.user_id,
            platform=entity.platform.value,
            topic=entity.topic,
            content=entity.content,
            hashtags=entity.hashtags,
            tone=entity.tone.value,
            language=entity.language.value,
            status=entity.status.value,
            tokens_used=entity.tokens_used,
            error_message=entity.error_message or None,
        )

    @staticmethod
    def update_orm(model: SocialPostModel, entity: SocialPost) -> None:
        model.user_id = entity.user_id
        model.platform = entity.platform.value
        model.topic = entity.topic
        model.content = entity.content
        model.hashtags = entity.hashtags
        model.tone = entity.tone.value
        model.language = entity.language.value
        model.status = entity.status.value
        model.tokens_used = entity.tokens_used
        model.error_message = entity.error_message or None
        model.updated_at = entity.updated_at
