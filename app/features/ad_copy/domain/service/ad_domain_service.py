"""
Domain service for Ad Copy feature.
Contains pure business logic — no infrastructure dependencies.
"""

from __future__ import annotations

from app.common.domain.domain_service import DomainService


class AdDomainService(DomainService):
    """Cross-entity domain logic for ad copy content."""

    PLATFORM_HEADLINE_LIMITS: dict[str, int] = {
        "google": 30,
        "facebook": 40,
    }

    PLATFORM_DESCRIPTION_LIMITS: dict[str, int] = {
        "google": 90,
        "facebook": 125,
    }

    @staticmethod
    def validate_headline_length(headline: str, platform: str) -> bool:
        """Check if headline fits within the platform's character limit."""
        limit = AdDomainService.PLATFORM_HEADLINE_LIMITS.get(platform.lower(), 40)
        return len(headline) <= limit

    @staticmethod
    def validate_description_length(description: str, platform: str) -> bool:
        """Check if description fits within the platform's character limit."""
        limit = AdDomainService.PLATFORM_DESCRIPTION_LIMITS.get(platform.lower(), 125)
        return len(description) <= limit
