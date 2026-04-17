from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateMetaCommand:
    """Command to generate SEO meta tags from content."""

    user_id: str = ""
    content: str = ""
    focus_keyword: str = ""
