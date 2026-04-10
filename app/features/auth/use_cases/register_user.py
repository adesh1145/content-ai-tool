"""
app/features/auth/use_cases/register_user.py
─────────────────────────────────────────────────────────────
RegisterUserUseCase — Layer 2: Application Business Rules.

SOLID:
  - SRP: Only handles user registration logic.
  - DIP: Depends on IUserRepository, not SQLAlchemy.
"""

from __future__ import annotations

from dataclasses import dataclass

from passlib.context import CryptContext

from app.core.exceptions import DuplicateError, ValidationError
from app.core.interfaces.base_use_case import IUseCase
from app.features.auth.entities.user import User
from app.features.auth.use_cases.interfaces.user_repo import IUserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class RegisterUserInput:
    email: str
    password: str
    full_name: str


@dataclass
class RegisterUserOutput:
    user_id: str
    email: str
    full_name: str


class RegisterUserUseCase(IUseCase[RegisterUserInput, RegisterUserOutput]):
    """Register a new user account."""

    def __init__(self, user_repo: IUserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, input_data: RegisterUserInput) -> RegisterUserOutput:
        # Domain validation
        if not input_data.email or "@" not in input_data.email:
            raise ValidationError("Invalid email address.")
        if len(input_data.password) < 8:
            raise ValidationError("Password must be at least 8 characters.")

        # Check for duplicate
        existing = await self._user_repo.get_by_email(input_data.email.lower())
        if existing:
            raise DuplicateError("User", "email", input_data.email)

        # Create entity and hash password
        user = User(
            email=input_data.email.lower().strip(),
            hashed_password=pwd_context.hash(input_data.password),
            full_name=input_data.full_name.strip(),
        )
        saved_user = await self._user_repo.save(user)

        return RegisterUserOutput(
            user_id=saved_user.id,
            email=saved_user.email,
            full_name=saved_user.full_name,
        )
