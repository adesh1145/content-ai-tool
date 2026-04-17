from __future__ import annotations

from pydantic import BaseModel


class RegisterResponse(BaseModel):
    user_id: str
    email: str
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    plan: str
    is_active: bool


class CreatedAPIKeyResponse(BaseModel):
    key_id: str
    name: str
    raw_key: str
    key_prefix: str
