from __future__ import annotations

from app.common.domain.value_objects import UserPlan
from app.features.auth.domain.model.api_key import APIKey
from app.features.auth.domain.model.email import Email
from app.features.auth.domain.model.hashed_password import HashedPassword
from app.features.auth.domain.model.user import User
from app.features.auth.infrastructure.persistence.entity import APIKeyModel, UserModel


class UserPersistenceMapper:
    """Maps between User aggregate root and UserModel ORM object."""

    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=Email(model.email),
            hashed_password=HashedPassword(model.hashed_password),
            full_name=model.full_name,
            plan=UserPlan(model.plan),
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            email=str(entity.email),
            hashed_password=str(entity.hashed_password),
            full_name=entity.full_name,
            plan=entity.plan.value,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: UserModel, entity: User) -> None:
        model.email = str(entity.email)
        model.full_name = entity.full_name
        model.plan = entity.plan.value
        model.is_active = entity.is_active
        model.is_verified = entity.is_verified


class APIKeyPersistenceMapper:
    """Maps between APIKey entity and APIKeyModel ORM object."""

    @staticmethod
    def to_domain(model: APIKeyModel) -> APIKey:
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

    @staticmethod
    def to_model(entity: APIKey) -> APIKeyModel:
        return APIKeyModel(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            key_hash=entity.key_hash,
            key_prefix=entity.key_prefix,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
