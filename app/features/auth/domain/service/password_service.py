from __future__ import annotations

from passlib.context import CryptContext

from app.features.auth.domain.model.hashed_password import HashedPassword

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """Domain service for password hashing and verification."""

    @staticmethod
    def hash(raw_password: str) -> HashedPassword:
        return HashedPassword(_pwd_context.hash(raw_password))

    @staticmethod
    def verify(raw_password: str, hashed: HashedPassword) -> bool:
        return _pwd_context.verify(raw_password, hashed.value)
