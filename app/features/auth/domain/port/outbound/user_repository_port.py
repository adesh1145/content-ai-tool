from __future__ import annotations

from abc import abstractmethod

from app.common.port.outbound.repository_port import RepositoryPort
from app.features.auth.domain.model.api_key import APIKey
from app.features.auth.domain.model.user import User


class IUserRepository(RepositoryPort[User]):
    """Abstract output port for User aggregate persistence."""

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
