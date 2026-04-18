from __future__ import annotations

import hashlib
import secrets

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.dependencies import get_current_user_id
from app.features.auth.config.container import AuthContainer
from app.features.auth.domain.event.api_key_created_event import APIKeyCreatedEvent
from app.features.auth.domain.model.api_key import APIKey
from app.features.auth.presentation.rest.dto.request import (
    CreateAPIKeyRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
)
from app.features.auth.presentation.rest.dto.response import (
    AccessTokenResponse,
    CreatedAPIKeyResponse,
    RegisterResponse,
    TokenResponse,
    UserProfileResponse,
)
from app.features.auth.presentation.rest.mapper import AuthRestMapper
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=ApiResponse[RegisterResponse], status_code=201)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse:
    container = AuthContainer(db)
    command = AuthRestMapper.to_register_command(body)
    result = await container.register_use_case.execute(command)
    return ApiResponse.ok(
        AuthRestMapper.to_register_response(result),
        message="User registered successfully.",
    )


@router.post("/login", response_model=ApiResponse[TokenResponse])
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse:
    container = AuthContainer(db)
    command = AuthRestMapper.to_login_command(body)
    result = await container.login_use_case.execute(command)
    return ApiResponse.ok(AuthRestMapper.to_token_response(result))


@router.post("/refresh", response_model=ApiResponse[AccessTokenResponse])
async def refresh_token(
    body: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse:
    container = AuthContainer(db)
    result = await container.refresh_use_case.execute(body.refresh_token)
    return ApiResponse.ok(AuthRestMapper.to_access_token_response(result))


@router.get("/me", response_model=ApiResponse[UserProfileResponse])
async def get_me(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse:
    container = AuthContainer(db)
    user = await container.user_repo.find_by_id(user_id)
    if not user:
        from app.features.auth.domain.exception.user_not_found import UserNotFoundError

        raise UserNotFoundError(user_id)
    from app.features.auth.application.result.user_result import UserResult

    user_result = UserResult(
        user_id=user.id,
        email=str(user.email),
        full_name=user.full_name,
        plan=user.plan.value,
        is_active=user.is_active,
    )
    return ApiResponse.ok(AuthRestMapper.to_user_profile_response(user_result))


@router.post("/api-keys", response_model=ApiResponse[CreatedAPIKeyResponse], status_code=201)
async def create_api_key(
    body: CreateAPIKeyRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
) -> ApiResponse:
    raw_key = f"cat-{secrets.token_urlsafe(32)}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    key_prefix = raw_key[:12]

    api_key = APIKey(
        user_id=user_id,
        name=body.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
    )

    container = AuthContainer(db)
    saved = await container.user_repo.save_api_key(api_key)

    await container.event_publisher.publish(
        APIKeyCreatedEvent(
            aggregate_id=user_id,
            key_name=body.name,
            key_prefix=key_prefix,
        )
    )

    return ApiResponse.ok(
        CreatedAPIKeyResponse(
            key_id=saved.id,
            name=saved.name,
            raw_key=raw_key,
            key_prefix=key_prefix,
        ),
        message="API key created. Store it securely — it won't be shown again.",
    )
