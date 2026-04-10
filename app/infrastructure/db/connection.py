"""
app/infrastructure/db/connection.py
─────────────────────────────────────────────────────────────
Async SQLAlchemy database connection management.

- Dev:  SQLite via aiosqlite
- Prod: PostgreSQL via asyncpg
  (switch by changing DATABASE_URL in .env)
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings

settings = get_settings()

# ── Engine ────────────────────────────────────────────────────────────────────

_connect_args: dict = {}
if settings.is_sqlite:
    _connect_args = {"check_same_thread": False}

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=_connect_args,
)

# ── Session factory ───────────────────────────────────────────────────────────

AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async DB session.

    Usage:
        async def endpoint(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_all_tables() -> None:
    """Create all SQLAlchemy tables (called on app startup)."""
    from app.infrastructure.db.base_model import Base  # noqa: PLC0415

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
