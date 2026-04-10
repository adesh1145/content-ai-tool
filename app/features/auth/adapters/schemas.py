"""
app/features/auth/adapters/schemas.py
─────────────────────────────────────────────────────────────
Pydantic DTOs for Auth feature API layer.
Layer 3: Interface Adapters — HTTP ↔ Use Case data mapping.
"""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


# ── Requests ──────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    full_name: str = Field(..., min_length=2, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CreateAPIKeyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=64, description="Name/label for this key")


# ── Responses ─────────────────────────────────────────────────────────────────

class RegisterResponse(BaseModel):
    user_id: str
    email: str
    full_name: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    plan: str
    is_active: bool


class APIKeyResponse(BaseModel):
    key_id: str
    name: str
    key_prefix: str    # First 8 chars — "sk-abc12..."
    is_active: bool
    created_at: str


class CreatedAPIKeyResponse(BaseModel):
    key_id: str
    name: str
    raw_key: str       # Shown ONCE at creation time
    key_prefix: str
