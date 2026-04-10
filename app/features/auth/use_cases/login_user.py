"""
app/features/auth/use_cases/login_user.py
─────────────────────────────────────────────────────────────
LoginUserUseCase — validates credentials, returns JWT tokens.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.interfaces.base_use_case import IUseCase
from app.features.auth.use_cases.interfaces.user_repo import IUserRepository

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class LoginInput:
    email: str
    password: str


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60


def _create_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


class LoginUserUseCase(IUseCase[LoginInput, TokenPair]):
    """Authenticate user credentials and issue JWT tokens."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, input_data: LoginInput) -> TokenPair:
        user = await self._user_repo.get_by_email(input_data.email.lower())

        if not user or not pwd_context.verify(input_data.password, user.hashed_password):
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationError("Account is deactivated.")

        access_token = _create_token(
            {"sub": user.id, "email": user.email, "type": "access"},
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = _create_token(
            {"sub": user.id, "type": "refresh"},
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return TokenPair(access_token=access_token, refresh_token=refresh_token)
