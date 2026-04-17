from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyzeSEOCommand:
    """Command to run comprehensive SEO analysis on content."""

    user_id: str = ""
    content: str = ""
    focus_keyword: str = ""
    meta_title: str = ""
    meta_description: str = ""
    url: str = ""
