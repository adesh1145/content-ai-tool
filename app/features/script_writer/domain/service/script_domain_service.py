from __future__ import annotations


class ScriptDomainService:
    """Domain service encoding script-related business rules."""

    @staticmethod
    def estimate_spoken_duration(word_count: int, wpm: int = 130) -> int:
        """Estimate spoken duration in seconds from word count."""
        if word_count <= 0 or wpm <= 0:
            return 0
        return round((word_count / wpm) * 60)
