from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.common.config.settings import get_settings
from app.common.exception.base_exception import AuthenticationException
from app.features.auth.domain.port.outbound.token_service_port import ITokenService

_settings = get_settings()


class JWTTokenService(ITokenService):
    """JWT implementation of ITokenService using python-jose."""

    def __init__(
        self,
        secret_key: str = _settings.SECRET_KEY,
        algorithm: str = _settings.JWT_ALGORITHM,
        access_expire_minutes: int = _settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_expire_days: int = _settings.REFRESH_TOKEN_EXPIRE_DAYS,
    ) -> None:
        self._secret = secret_key
        self._algorithm = algorithm
        self._access_expire_minutes = access_expire_minutes
        self._refresh_expire_days = refresh_expire_days

    def _encode(self, payload: dict, expires_delta: timedelta) -> str:
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(data, self._secret, algorithm=self._algorithm)

    def create_access_token(self, user_id: str, email: str) -> str:
        return self._encode(
            {"sub": user_id, "email": email, "type": "access"},
            timedelta(minutes=self._access_expire_minutes),
        )

    def create_refresh_token(self, user_id: str) -> str:
        return self._encode(
            {"sub": user_id, "type": "refresh"},
            timedelta(days=self._refresh_expire_days),
        )

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except JWTError as exc:
            raise AuthenticationException(f"Invalid or expired token: {exc}")

    def get_access_token_expire_seconds(self) -> int:
        return self._access_expire_minutes * 60
