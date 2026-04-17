from __future__ import annotations

from abc import ABC, abstractmethod


class ITokenService(ABC):
    """Output port for JWT token operations."""

    @abstractmethod
    def create_access_token(self, user_id: str, email: str) -> str: ...

    @abstractmethod
    def create_refresh_token(self, user_id: str) -> str: ...

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        """Decode and verify a token. Raises AuthenticationException on failure."""
        ...

    @abstractmethod
    def get_access_token_expire_seconds(self) -> int: ...
