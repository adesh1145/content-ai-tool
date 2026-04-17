from __future__ import annotations

import math

from app.common.domain.domain_service import DomainService


class BlogDomainService(DomainService):
    """Cross-entity domain logic for blog content quality assessment."""

    @staticmethod
    def calculate_reading_time(word_count: int, wpm: int = 200) -> int:
        """Estimated reading time in minutes (min 1)."""
        return max(1, math.ceil(word_count / wpm))

    @staticmethod
    def calculate_readability_score(text: str) -> float:
        """
        Flesch-Kincaid readability score.

        Uses textstat when available; falls back to a lightweight approximation
        so the domain layer stays free of heavy third-party dependencies.
        """
        try:
            import textstat  # noqa: PLC0415
            return float(textstat.flesch_reading_ease(text))
        except ImportError:
            sentences = max(1, text.count(".") + text.count("!") + text.count("?"))
            words = text.split()
            total_words = max(1, len(words))
            syllables = sum(_estimate_syllables(w) for w in words)
            return (
                206.835
                - 1.015 * (total_words / sentences)
                - 84.6 * (syllables / total_words)
            )


def _estimate_syllables(word: str) -> int:
    word = word.lower().strip(".,!?;:")
    if len(word) <= 3:
        return 1
    vowels = "aeiou"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e"):
        count = max(1, count - 1)
    return max(1, count)
