"""
Domain service for Social Media feature.
Contains pure business logic — no infrastructure dependencies.
"""

from __future__ import annotations

from app.common.domain.domain_service import DomainService


class SocialDomainService(DomainService):
    """Cross-entity domain logic for social media content."""

    PLATFORM_CHAR_LIMITS: dict[str, int] = {
        "twitter": 280,
        "linkedin": 3000,
        "instagram": 2200,
    }

    @staticmethod
    def get_char_limit(platform: str) -> int:
        """Return the character limit for a platform."""
        return SocialDomainService.PLATFORM_CHAR_LIMITS.get(
            platform.lower(), 3000
        )

    @staticmethod
    def is_within_limit(content: str, platform: str) -> bool:
        """Check if content fits within the platform's character limit."""
        limit = SocialDomainService.get_char_limit(platform)
        return len(content) <= limit

    @staticmethod
    def count_hashtags(content: str) -> int:
        """Count the number of hashtags in the content."""
        import re
        return len(re.findall(r"#\w+", content))
