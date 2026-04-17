from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MetaResult:
    """Result returned by the generate-meta use case."""

    meta_title: str = ""
    meta_description: str = ""
    slug: str = ""
    tokens_used: int = 0
