"""
app/dependencies.py
─────────────────────────────────────────────────────────────
Global FastAPI dependency injection providers.

Usage in routes:
    async def endpoint(
        db: AsyncSession = Depends(get_db),
        current_user_id: str = Depends(get_current_user_id),
        llm: ILLMProvider = Depends(get_llm),
    ): ...
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.interfaces.llm_provider import ILLMProvider
from app.infrastructure.ai.llm_factory import get_llm_provider
from app.infrastructure.db.connection import get_db_session

settings = get_settings()
security = HTTPBearer()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency."""
    async for session in get_db_session():
        yield session


def get_llm() -> ILLMProvider:
    """LLM provider dependency (singleton)."""
    return get_llm_provider()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> str:
    """
    JWT auth dependency — extract user_id from Bearer token.

    Usage:
        user_id: str = Depends(get_current_user_id)
    """
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user ID.")
        return user_id
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token invalid or expired: {e}")
