from __future__ import annotations

from app.common.exception.base_exception import AuthenticationException
from app.features.auth.application.result.token_result import AccessTokenResult
from app.features.auth.domain.port.inbound.refresh_token_port import IRefreshToken
from app.features.auth.domain.port.outbound.token_service_port import ITokenService
from app.features.auth.domain.port.outbound.user_repository_port import IUserRepository


class RefreshTokenService(IRefreshToken):
    """Validate a refresh token and issue a new access token."""

    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenService,
    ) -> None:
        self._user_repo = user_repo
        self._token_service = token_service

    async def execute(self, input_data: str) -> AccessTokenResult:
        payload = self._token_service.verify_token(input_data)

        if payload.get("type") != "refresh":
            raise AuthenticationException("Invalid token type. Expected refresh token.")

        user_id = payload.get("sub")
        if not user_id:
            raise AuthenticationException("Invalid refresh token payload.")

        user = await self._user_repo.find_by_id(user_id)
        if not user:
            raise AuthenticationException("User not found.")
        if not user.is_active:
            raise AuthenticationException("Account is deactivated.")

        access_token = self._token_service.create_access_token(
            user_id=user.id, email=str(user.email)
        )

        return AccessTokenResult(
            access_token=access_token,
            expires_in=self._token_service.get_access_token_expire_seconds(),
        )
