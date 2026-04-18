"""
Domain service for Email Writer feature.
Contains pure business logic — no infrastructure dependencies.
"""

from __future__ import annotations

from app.common.domain.domain_service import DomainService


class EmailDomainService(DomainService):
    """Cross-entity domain logic for email content."""

    RECOMMENDED_WORD_COUNTS: dict[str, int] = {
        "cold_email": 150,
        "newsletter": 500,
        "followup": 100,
        "welcome": 200,
    }

    @staticmethod
    def get_recommended_word_count(email_type: str) -> int:
        """Return the recommended word count for an email type."""
        return EmailDomainService.RECOMMENDED_WORD_COUNTS.get(email_type, 200)

    @staticmethod
    def validate_subject_line_length(subject: str) -> bool:
        """Subject lines should be 30-80 characters for best open rates."""
        return 30 <= len(subject) <= 80
