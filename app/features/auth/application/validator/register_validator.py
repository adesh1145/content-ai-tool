from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.auth.application.command.register_command import RegisterCommand


class RegisterValidator:
    """Validates registration input before the domain layer is invoked."""

    MIN_PASSWORD_LENGTH = 8

    @classmethod
    def validate(cls, command: RegisterCommand) -> None:
        if not command.email or "@" not in command.email:
            raise ValidationException("Invalid email address.")

        if len(command.password) < cls.MIN_PASSWORD_LENGTH:
            raise ValidationException(
                f"Password must be at least {cls.MIN_PASSWORD_LENGTH} characters."
            )

        if not command.full_name or not command.full_name.strip():
            raise ValidationException("Full name is required.")
