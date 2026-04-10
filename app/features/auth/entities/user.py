"""
app/features/auth/entities/user.py
─────────────────────────────────────────────────────────────
User domain entity (Layer 1 — Enterprise Business Rules).
Zero external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.entities.base_entity import BaseEntity
from app.core.entities.value_objects import UserPlan


@dataclass
class User(BaseEntity):
    email: str = ""
    hashed_password: str = ""
    full_name: str = ""
    plan: UserPlan = UserPlan.FREE
    is_active: bool = True
    is_verified: bool = False

    def is_pro(self) -> bool:
        return self.plan in (UserPlan.PRO, UserPlan.ENTERPRISE)

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()

    def upgrade_plan(self, new_plan: UserPlan) -> None:
        self.plan = new_plan
        self.touch()


@dataclass
class APIKey(BaseEntity):
    user_id: str = ""
    name: str = ""
    key_hash: str = ""           # Store only hash, never raw key
    key_prefix: str = ""         # First 8 chars for display (e.g. "sk-abc12")
    is_active: bool = True
    last_used_at: str | None = None

    def revoke(self) -> None:
        self.is_active = False
        self.touch()
