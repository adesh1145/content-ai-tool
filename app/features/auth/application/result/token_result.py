from __future__ import annotations

from pydantic import BaseModel


class TokenResult(BaseModel):
    """Full token pair returned after successful login."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 0


class AccessTokenResult(BaseModel):
    """Single access token returned after a refresh."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = 0
