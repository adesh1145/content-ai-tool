"""
app/features/auth/use_cases/interfaces/user_repo.py
─────────────────────────────────────────────────────────────
IUserRepository — abstract contract for user persistence.

Use cases depend on this, NOT on SQLAlchemy models.
"""

from __future__ import annotations

from abc import abstractmethod

from app.core.interfaces.base_repository import IRepository
from app.features.auth.entities.user import APIKey, User


class IUserRepository(IRepository[User]):
    """User-specific repository contract."""

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def list_api_keys(self, user_id: str) -> list[APIKey]: ...

    @abstractmethod
    async def save_api_key(self, api_key: APIKey) -> APIKey: ...

    @abstractmethod
    async def get_api_key_by_hash(self, key_hash: str) -> APIKey | None: ...

    @abstractmethod
    async def revoke_api_key(self, key_id: str, user_id: str) -> bool: ...
