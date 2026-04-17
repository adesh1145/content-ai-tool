"""
app/features/auth/use_cases/refresh_token.py
─────────────────────────────────────────────────────────────
RefreshTokenUseCase — validates refresh token and issues a new access token.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.interfaces.base_use_case import IUseCase
from app.features.auth.use_cases.interfaces.user_repo import IUserRepository

settings = get_settings()


@dataclass
class RefreshTokenInput:
    refresh_token: str


@dataclass
class RefreshTokenOutput:
    access_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


def _create_access_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


class RefreshTokenUseCase(IUseCase[RefreshTokenInput, RefreshTokenOutput]):
    """Consume a valid refresh token and issue a new access token."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, input_data: RefreshTokenInput) -> RefreshTokenOutput:
        try:
            payload = jwt.decode(
                input_data.refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except JWTError:
            raise AuthenticationError("Invalid or expired refresh token.")

        if payload.get("type") != "refresh":
            raise AuthenticationError("Invalid token type. Expected refresh token.")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Invalid refresh token payload.")

        # Ensure user still exists and is active
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise AuthenticationError("User not found.")
        if not user.is_active:
            raise AuthenticationError("Account is deactivated.")

        # Issue new access token
        access_token = _create_access_token(
            {"sub": user.id, "email": user.email, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return RefreshTokenOutput(access_token=access_token)
