from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.base_entity import BaseEntity


@dataclass
class APIKey(BaseEntity):
    """API key entity belonging to a User aggregate."""

    user_id: str = ""
    name: str = ""
    key_hash: str = ""
    key_prefix: str = ""
    is_active: bool = True
    last_used_at: str | None = None

    def revoke(self) -> None:
        self.is_active = False
        self.touch()
