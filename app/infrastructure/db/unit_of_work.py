from __future__ import annotations

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.application.unit_of_work import UnitOfWork as IUnitOfWork
from app.infrastructure.db.connection import AsyncSessionFactory


class SqlAlchemyUnitOfWork(IUnitOfWork):
    """SQLAlchemy implementation of the Unit of Work pattern."""

    def __init__(self) -> None:
        self._session: AsyncSession | None = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("UnitOfWork not entered. Use 'async with' context manager.")
        return self._session

    async def __aenter__(self) -> SqlAlchemyUnitOfWork:
        self._session = AsyncSessionFactory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        await self.session.close()
        self._session = None

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
