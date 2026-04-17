from __future__ import annotations

from dataclasses import dataclass, field

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import GenerationStatus, Language, SocialPlatform, Tone
from app.features.social_media.domain.event.social_post_created_event import (
    SocialPostCreatedEvent,
)


@dataclass
class SocialPost(AggregateRoot):
    """Aggregate root for a social-media post generation."""

    user_id: str = ""
    platform: SocialPlatform = SocialPlatform.LINKEDIN
    topic: str = ""
    content: str = ""
    hashtags: list[str] = field(default_factory=list)
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str = ""

    def complete_generation(
        self, content: str, hashtags: list[str], tokens: int
    ) -> None:
        self.content = content
        self.hashtags = hashtags
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            SocialPostCreatedEvent(
                aggregate_id=self.id,
                aggregate_type="SocialPost",
                platform=self.platform.value,
                topic=self.topic,
                char_count=len(content),
                user_id=self.user_id,
            )
        )

    def fail_generation(self, error: str) -> None:
        self.status = GenerationStatus.FAILED
        self.error_message = error
        self.touch()
