from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    message: str = ""

    @classmethod
    def ok(cls, data: T | None = None, message: str = "") -> ApiResponse[T]:
        return cls(success=True, data=data, message=message)

    @classmethod
    def error(cls, message: str, data: Any = None) -> ApiResponse[Any]:
        return cls(success=False, data=data, message=message)


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T] = []
    total: int = 0
    page: int = 1
    size: int = 20
    pages: int = 0
