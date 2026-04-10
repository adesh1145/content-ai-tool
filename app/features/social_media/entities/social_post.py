"""
app/features/social_media/entities/social_post.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from app.core.entities.base_entity import BaseEntity
from app.core.entities.value_objects import GenerationStatus, Language, SocialPlatform, Tone


@dataclass
class SocialPost(BaseEntity):
    user_id: str = ""
    platform: SocialPlatform = SocialPlatform.LINKEDIN
    topic: str = ""
    caption: str = ""
    hashtags: list[str] = field(default_factory=list)
    cta: str = ""              # Call to action
    emoji_used: bool = True
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    char_count: int = 0
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0

    # Platform-specific limits
    PLATFORM_LIMITS: dict = field(default_factory=lambda: {
        "linkedin": 3000,
        "twitter": 280,
        "instagram": 2200,
    })

    def is_within_limit(self) -> bool:
        limit = self.PLATFORM_LIMITS.get(self.platform.value, 3000)
        return len(self.caption) <= limit
