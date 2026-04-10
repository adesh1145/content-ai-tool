"""
app/features/auth/adapters/user_gateway.py
─────────────────────────────────────────────────────────────
IUserRepository implementation using SQLAlchemy.
Layer 3: Interface Adapters (Gateway pattern).

Translates between domain entities (User) and DB models (UserModel).
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.auth.entities.user import APIKey, User
from app.features.auth.use_cases.interfaces.user_repo import IUserRepository
from app.features.auth.drivers.models import APIKeyModel, UserModel


def _model_to_user(model: UserModel) -> User:
    from app.core.entities.value_objects import UserPlan
    return User(
        id=model.id,
        email=model.email,
        hashed_password=model.hashed_password,
        full_name=model.full_name,
        plan=UserPlan(model.plan),
        is_active=model.is_active,
        is_verified=model.is_verified,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _model_to_api_key(model: APIKeyModel) -> APIKey:
    return APIKey(
        id=model.id,
        user_id=model.user_id,
        name=model.name,
        key_hash=model.key_hash,
        key_prefix=model.key_prefix,
        is_active=model.is_active,
        last_used_at=model.last_used_at,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


class UserGateway(IUserRepository):
    """SQLAlchemy implementation of IUserRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entity: User) -> User:
        existing = await self._session.get(UserModel, entity.id)
        if existing:
            existing.email = entity.email
            existing.full_name = entity.full_name
            existing.plan = entity.plan.value
            existing.is_active = entity.is_active
            existing.is_verified = entity.is_verified
        else:
            model = UserModel(
                id=entity.id,
                email=entity.email,
                hashed_password=entity.hashed_password,
                full_name=entity.full_name,
                plan=entity.plan.value,
                is_active=entity.is_active,
                is_verified=entity.is_verified,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            )
            self._session.add(model)

        await self._session.flush()
        return entity

    async def get_by_id(self, entity_id: str) -> User | None:
        model = await self._session.get(UserModel, entity_id)
        return _model_to_user(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return _model_to_user(model) if model else None

    async def delete(self, entity_id: str) -> bool:
        model = await self._session.get(UserModel, entity_id)
        if not model:
            return False
        await self._session.delete(model)
        return True

    async def list_api_keys(self, user_id: str) -> list[APIKey]:
        result = await self._session.execute(
            select(APIKeyModel).where(
                APIKeyModel.user_id == user_id,
                APIKeyModel.is_active == True,
            )
        )
        return [_model_to_api_key(m) for m in result.scalars().all()]

    async def save_api_key(self, api_key: APIKey) -> APIKey:
        model = APIKeyModel(
            id=api_key.id,
            user_id=api_key.user_id,
            name=api_key.name,
            key_hash=api_key.key_hash,
            key_prefix=api_key.key_prefix,
            is_active=api_key.is_active,
            created_at=api_key.created_at,
            updated_at=api_key.updated_at,
        )
        self._session.add(model)
        await self._session.flush()
        return api_key

    async def get_api_key_by_hash(self, key_hash: str) -> APIKey | None:
        result = await self._session.execute(
            select(APIKeyModel).where(APIKeyModel.key_hash == key_hash)
        )
        model = result.scalar_one_or_none()
        return _model_to_api_key(model) if model else None

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
