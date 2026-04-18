from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.script_writer.infrastructure.persistence.entity import ScriptModel
from app.features.script_writer.infrastructure.persistence.mapper import ScriptORMMapper
from app.features.script_writer.domain.model.script import Script
from app.features.script_writer.domain.port.outbound.script_repository_port import (
    IScriptRepository,
)


class ScriptRepositoryImpl(IScriptRepository):
    """Driven adapter — persists Script aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: Script) -> Script:
        existing = await self._session.get(ScriptModel, entity.id)
        if existing:
            ScriptORMMapper.update_model(existing, entity)
        else:
            model = ScriptORMMapper.to_model(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> Script | None:
        model = await self._session.get(ScriptModel, id)
        return ScriptORMMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[Script]:
        result = await self._session.execute(
            select(ScriptModel).offset(skip).limit(limit).order_by(ScriptModel.created_at.desc())
        )
        return [ScriptORMMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(ScriptModel, id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def find_by_user_id(self, user_id: str) -> list[Script]:
        result = await self._session.execute(
            select(ScriptModel)
            .where(ScriptModel.user_id == user_id)
            .order_by(ScriptModel.created_at.desc())
        )
        return [ScriptORMMapper.to_domain(m) for m in result.scalars().all()]
