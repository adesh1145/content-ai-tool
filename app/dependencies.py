"""
app/dependencies.py
─────────────────────────────────────────────────────────────
Global FastAPI dependency injection providers.

LLM NOTE: There is NO global `get_llm()` dependency here.
Model selection is per-feature — each feature's container wires
its own AI service with the right provider+model from model_config.py.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.config.settings import get_settings
from app.infrastructure.db.connection import get_db_session

settings = get_settings()
security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session():
        yield session


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> str:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID.")
        return user_id
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token invalid or expired: {e}")
