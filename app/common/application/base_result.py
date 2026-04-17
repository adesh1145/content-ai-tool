from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseResult(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    message: str = ""
    errors: list[str] | None = None

    @classmethod
    def ok(cls, data: T, message: str = "") -> BaseResult[T]:
        return cls(success=True, data=data, message=message)

    @classmethod
    def fail(cls, message: str, errors: list[str] | None = None) -> BaseResult[Any]:
        return cls(success=False, message=message, errors=errors)
