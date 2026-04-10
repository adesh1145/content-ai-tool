"""
app/core/entities/base_entity.py
─────────────────────────────────────────────────────────────
Base domain entity shared by all features.

Clean Architecture Layer 1: Enterprise Business Rules.
Zero external dependencies — pure Python only.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class BaseEntity:
    """
    Root base for all domain entities.

    Rules:
    - Pure Python — NO SQLAlchemy, NO Pydantic, NO FastAPI imports here.
    - Identity is a UUID string (serialisable, DB-agnostic).
    - Timestamps are always UTC-aware.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=_utcnow)
    updated_at: datetime = field(default_factory=_utcnow)

    def touch(self) -> None:
        """Update the `updated_at` timestamp (call before persisting changes)."""
        self.updated_at = _utcnow()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
