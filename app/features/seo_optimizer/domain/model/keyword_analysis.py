from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KeywordAnalysis:
    """Value object representing the analysis of a single keyword within content."""

    keyword: str = ""
    density_percent: float = 0.0
    occurrences: int = 0
    is_in_title: bool = False
    is_in_first_paragraph: bool = False
    is_in_headings: bool = False
    recommendation: str = ""
