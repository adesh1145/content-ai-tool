from __future__ import annotations

from app.common.exception.base_exception import ValidationException


class Email:
    """Immutable value object representing a validated email address."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        normalised = value.strip().lower()
        if normalised and "@" not in normalised:
            raise ValidationException(f"Invalid email address: '{value}'")
        self._value = normalised

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"Email('{self._value}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self._value == other._value
        if isinstance(other, str):
            return self._value == other.strip().lower()
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self._value)
