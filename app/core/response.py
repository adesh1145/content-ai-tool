"""
app/core/response.py
─────────────────────────────────────────────────────────────
Unified API response envelope — all endpoints return this shape.

Provides consistent structure for clients:
  { "success": bool, "data": T | None, "message": str, "error_code": str | None }
"""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    """Standard API response wrapper used by all endpoints."""

    success: bool
    data: DataT | None = None
    message: str = "OK"
    error_code: str | None = None

    @classmethod
    def ok(cls, data: DataT, message: str = "Success") -> APIResponse[DataT]:
        return cls(success=True, data=data, message=message)

    @classmethod
    def error(cls, message: str, error_code: str = "ERROR") -> APIResponse[None]:
        return cls(success=False, data=None, message=message, error_code=error_code)


class PagedResponse(BaseModel, Generic[DataT]):
    """Paginated list response wrapper."""

    success: bool = True
    data: list[DataT]
    total: int
    page: int
    page_size: int
    has_next: bool

    @property
    def total_pages(self) -> int:
        return -(-self.total // self.page_size)  # ceiling division
