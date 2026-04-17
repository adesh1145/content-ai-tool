from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.email_writer.adapter.outbound.persistence.entity import EmailContentModel
from app.features.email_writer.adapter.outbound.persistence.mapper import EmailContentMapper
from app.features.email_writer.domain.model.email_content import EmailContent
from app.features.email_writer.domain.port.outbound.email_repository_port import EmailRepositoryPort


class EmailRepositoryImpl(EmailRepositoryPort):
    """Driven adapter — persists EmailContent aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: EmailContent) -> EmailContent:
        existing = await self._session.get(EmailContentModel, entity.id)
        if existing:
            EmailContentMapper.update_model(existing, entity)
        else:
            model = EmailContentMapper.to_model(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> EmailContent | None:
        model = await self._session.get(EmailContentModel, id)
        return EmailContentMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[EmailContent]:
        result = await self._session.execute(
            select(EmailContentModel).offset(skip).limit(limit)
        )
        return [EmailContentMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(EmailContentModel, id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def find_by_user_id(self, user_id: str) -> list[EmailContent]:
        result = await self._session.execute(
            select(EmailContentModel)
            .where(EmailContentModel.user_id == user_id)
            .order_by(EmailContentModel.created_at.desc())
        )
        return [EmailContentMapper.to_domain(m) for m in result.scalars().all()]
