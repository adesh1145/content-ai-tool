from __future__ import annotations

from app.common.exception.base_exception import AuthenticationException


class InvalidCredentialsError(AuthenticationException):
    """Raised when login credentials are invalid."""

    def __init__(self, message: str = "Invalid email or password.") -> None:
        super().__init__(message=message)
