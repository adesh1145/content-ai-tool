from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.adapter.outbound.persistence.entity import APIKeyModel, UserModel
from app.features.auth.adapter.outbound.persistence.mapper import (
    APIKeyPersistenceMapper,
    UserPersistenceMapper,
)
from app.features.auth.domain.model.api_key import APIKey
from app.features.auth.domain.model.user import User
from app.features.auth.domain.port.outbound.user_repository_port import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    """Driven adapter — SQLAlchemy implementation of IUserRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: User) -> User:
        existing = await self._session.get(UserModel, entity.id)
        if existing:
            UserPersistenceMapper.update_model(existing, entity)
        else:
            model = UserPersistenceMapper.to_model(entity)
            self._session.add(model)
        await self._session.flush()
        return entity

    async def find_by_id(self, id: str) -> User | None:
        model = await self._session.get(UserModel, id)
        return UserPersistenceMapper.to_domain(model) if model else None

    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self._session.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        return [UserPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def delete(self, id: str) -> bool:
        model = await self._session.get(UserModel, id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return UserPersistenceMapper.to_domain(model) if model else None

    async def list_api_keys(self, user_id: str) -> list[APIKey]:
        result = await self._session.execute(
            select(APIKeyModel).where(
                APIKeyModel.user_id == user_id,
                APIKeyModel.is_active == True,  # noqa: E712
            )
        )
        return [APIKeyPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def save_api_key(self, api_key: APIKey) -> APIKey:
        model = APIKeyPersistenceMapper.to_model(api_key)
        self._session.add(model)
        await self._session.flush()
        return api_key

    async def get_api_key_by_hash(self, key_hash: str) -> APIKey | None:
        result = await self._session.execute(
            select(APIKeyModel).where(APIKeyModel.key_hash == key_hash)
        )
        model = result.scalar_one_or_none()
        return APIKeyPersistenceMapper.to_domain(model) if model else None

    async def revoke_api_key(self, key_id: str, user_id: str) -> bool:
        result = await self._session.execute(
            select(APIKeyModel).where(
                APIKeyModel.id == key_id,
                APIKeyModel.user_id == user_id,
            )
        )
        model = result.scalar_one_or_none()
        if not model:
            return False
        model.is_active = False
        return True
