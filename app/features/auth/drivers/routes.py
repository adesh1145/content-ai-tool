"""
app/features/auth/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI router for Auth feature.
Layer 4: Frameworks & Drivers.
"""

from __future__ import annotations

import hashlib
import secrets

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.exceptions import AuthenticationError, DomainException, DuplicateError, ValidationError
from app.core.response import APIResponse
from app.features.auth.adapters.schemas import (
    CreateAPIKeyRequest,
    CreatedAPIKeyResponse,
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
    UserProfileResponse,
)
from app.features.auth.adapters.user_gateway import UserGateway
from app.features.auth.entities.user import APIKey
from app.features.auth.use_cases.login_user import LoginInput, LoginUserUseCase
from app.features.auth.use_cases.register_user import RegisterUserInput, RegisterUserUseCase
from app.infrastructure.db.connection import get_db_session

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Authentication"])


def _get_current_user_id(token: str) -> str:
    """Decode JWT and return user_id (sub claim)."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise AuthenticationError("Invalid token payload.")
        return user_id
    except JWTError as e:
        raise AuthenticationError(f"Token validation failed: {e}") from e


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/register", response_model=APIResponse[RegisterResponse], status_code=201)
async def register(
    body: RegisterRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """Register a new user account."""
    try:
        use_case = RegisterUserUseCase(UserGateway(db))
        result = await use_case.execute(
            RegisterUserInput(
                email=body.email,
                password=body.password,
                full_name=body.full_name,
            )
        )
        return APIResponse.ok(
            RegisterResponse(
                user_id=result.user_id,
                email=result.email,
                full_name=result.full_name,
            ),
            message="User registered successfully.",
        )
    except DuplicateError as e:
        raise HTTPException(status_code=409, detail=e.message)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """Login and receive JWT access + refresh token."""
    try:
        use_case = LoginUserUseCase(UserGateway(db))
        tokens = await use_case.execute(LoginInput(email=body.email, password=body.password))
        return APIResponse.ok(
            TokenResponse(
                access_token=tokens.access_token,
                refresh_token=tokens.refresh_token,
                expires_in=tokens.expires_in,
            )
        )
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.get("/me", response_model=APIResponse[UserProfileResponse])
async def get_me(
    token: str = Depends(lambda: None),  # Auth header handled by dependency
    db: AsyncSession = Depends(get_db_session),
):
    """Get current authenticated user profile."""
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
    raise HTTPException(status_code=501, detail="Use Authorization: Bearer <token>")


@router.post("/api-keys", response_model=APIResponse[CreatedAPIKeyResponse], status_code=201)
async def create_api_key(
    body: CreateAPIKeyRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """Create a new API key. The raw key is shown ONCE — store it securely."""
    raw_key = f"cat-{secrets.token_urlsafe(32)}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    key_prefix = raw_key[:12]

    # NOTE: In real usage this would require auth; simplified for scaffold
    api_key = APIKey(
        user_id="demo-user",
        name=body.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
    )
    gateway = UserGateway(db)
    saved = await gateway.save_api_key(api_key)

    return APIResponse.ok(
        CreatedAPIKeyResponse(
            key_id=saved.id,
            name=saved.name,
            raw_key=raw_key,
            key_prefix=key_prefix,
        ),
        message="API key created. Store it securely — it won't be shown again.",
    )
