from __future__ import annotations

from dataclasses import dataclass

import textstat


@dataclass
class ReadabilityResult:
    """Result of a readability analysis."""

    flesch_reading_ease: float = 0.0
    flesch_kincaid_grade: float = 0.0
    avg_sentence_length: float = 0.0
    readability_score: float = 0.0


class ReadabilityService:
    """Domain service for analysing content readability using textstat."""

    @staticmethod
    def analyze(text: str) -> ReadabilityResult:
        if not text or not text.strip():
            return ReadabilityResult()

        fre = textstat.flesch_reading_ease(text)
        fkg = textstat.flesch_kincaid_grade(text)
        sentence_count = textstat.sentence_count(text)
        word_count = textstat.lexicon_count(text, removepunct=True)
        avg_sentence_length = word_count / max(sentence_count, 1)

        readability_score = min(max(fre, 0), 100)

        return ReadabilityResult(
            flesch_reading_ease=round(fre, 2),
            flesch_kincaid_grade=round(fkg, 2),
            avg_sentence_length=round(avg_sentence_length, 2),
            readability_score=round(readability_score, 2),
        )
