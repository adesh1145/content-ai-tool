from __future__ import annotations

from dataclasses import dataclass, field

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import UserPlan
from app.features.auth.domain.model.email import Email
from app.features.auth.domain.model.hashed_password import HashedPassword


@dataclass
class User(AggregateRoot):
    """User aggregate root — the central identity in the Auth bounded context."""

    email: Email = field(default_factory=lambda: Email(""))
    hashed_password: HashedPassword = field(default_factory=lambda: HashedPassword(""))
    full_name: str = ""
    plan: UserPlan = UserPlan.FREE
    is_active: bool = True
    is_verified: bool = False

    def is_pro(self) -> bool:
        return self.plan in (UserPlan.PRO, UserPlan.ENTERPRISE)

    def deactivate(self) -> None:
        self.is_active = False
        self.touch()

    def activate(self) -> None:
        self.is_active = True
        self.touch()

    def upgrade_plan(self, new_plan: UserPlan) -> None:
        self.plan = new_plan
        self.touch()

    def verify(self) -> None:
        self.is_verified = True
        self.touch()
