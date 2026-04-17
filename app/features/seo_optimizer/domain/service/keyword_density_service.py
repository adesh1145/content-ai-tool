from __future__ import annotations

import re

from app.features.seo_optimizer.domain.model.keyword_analysis import KeywordAnalysis


class KeywordDensityService:
    """Domain service for analysing keyword density within content."""

    @staticmethod
    def analyze(content: str, keyword: str) -> KeywordAnalysis:
        if not content or not keyword:
            return KeywordAnalysis(keyword=keyword)

        content_lower = content.lower()
        keyword_lower = keyword.lower().strip()

        words = re.findall(r"\b\w+\b", content_lower)
        word_count = len(words)
        if word_count == 0:
            return KeywordAnalysis(keyword=keyword)

        occurrences = content_lower.count(keyword_lower)
        keyword_word_count = len(keyword_lower.split())
        density = (occurrences * keyword_word_count / word_count) * 100 if word_count else 0

        lines = content.split("\n")
        first_paragraph = ""
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                first_paragraph = stripped
                break

        headings = [l.strip().lstrip("#").strip().lower() for l in lines if l.strip().startswith("#")]
        is_in_headings = any(keyword_lower in h for h in headings)
        title_lines = [l for l in lines if l.strip().startswith("# ")]
        is_in_title = any(keyword_lower in t.lower() for t in title_lines)
        is_in_first_paragraph = keyword_lower in first_paragraph.lower()

        recommendation = ""
        if density < 0.5:
            recommendation = f"Keyword '{keyword}' density is low ({density:.1f}%). Consider increasing usage."
        elif density > 3.0:
            recommendation = f"Keyword '{keyword}' density is high ({density:.1f}%). Reduce to avoid keyword stuffing."
        else:
            recommendation = f"Keyword '{keyword}' density ({density:.1f}%) is within optimal range."

        return KeywordAnalysis(
            keyword=keyword,
            density_percent=round(density, 2),
            occurrences=occurrences,
            is_in_title=is_in_title,
            is_in_first_paragraph=is_in_first_paragraph,
            is_in_headings=is_in_headings,
            recommendation=recommendation,
        )
