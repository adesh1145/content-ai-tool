from __future__ import annotations

import math

from app.common.exception.base_exception import ValidationException


class ArticleDomainService:
    """Pure domain logic for article validation and calculations."""

    AVERAGE_READING_WPM = 238

    @staticmethod
    def validate_article_request(topic: str, word_count: int) -> None:
        if len(topic.strip()) < 10:
            raise ValidationException("Topic must be at least 10 characters long.")
        if not 500 <= word_count <= 5000:
            raise ValidationException("Word count target must be between 500 and 5000.")

    @staticmethod
    def estimate_reading_time(word_count: int) -> int:
        return max(1, math.ceil(word_count / ArticleDomainService.AVERAGE_READING_WPM))
