from __future__ import annotations

from app.features.auth.adapter.inbound.web.dto.request import LoginRequest, RegisterRequest
from app.features.auth.adapter.inbound.web.dto.response import (
    AccessTokenResponse,
    RegisterResponse,
    TokenResponse,
    UserProfileResponse,
)
from app.features.auth.application.command.login_command import LoginCommand
from app.features.auth.application.command.register_command import RegisterCommand
from app.features.auth.application.result.token_result import AccessTokenResult, TokenResult
from app.features.auth.application.result.user_result import UserResult


class AuthWebMapper:
    """Maps between web-layer DTOs and application-layer commands/results."""

    @staticmethod
    def to_register_command(req: RegisterRequest) -> RegisterCommand:
        return RegisterCommand(
            email=req.email,
            password=req.password,
            full_name=req.full_name,
        )

    @staticmethod
    def to_login_command(req: LoginRequest) -> LoginCommand:
        return LoginCommand(email=req.email, password=req.password)

    @staticmethod
    def to_register_response(result: UserResult) -> RegisterResponse:
        return RegisterResponse(
            user_id=result.user_id,
            email=result.email,
            full_name=result.full_name,
        )

    @staticmethod
    def to_token_response(result: TokenResult) -> TokenResponse:
        return TokenResponse(
            access_token=result.access_token,
            refresh_token=result.refresh_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
        )

    @staticmethod
    def to_access_token_response(result: AccessTokenResult) -> AccessTokenResponse:
        return AccessTokenResponse(
            access_token=result.access_token,
            token_type=result.token_type,
            expires_in=result.expires_in,
        )

    @staticmethod
    def to_user_profile_response(result: UserResult) -> UserProfileResponse:
        return UserProfileResponse(
            user_id=result.user_id,
            email=result.email,
            full_name=result.full_name,
            plan=result.plan,
            is_active=result.is_active,
        )
