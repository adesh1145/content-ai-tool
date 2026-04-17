from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseQuery(BaseModel):
    """Marker base for all queries (input DTOs for read operations)."""
    pass


class QueryHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, query: BaseQuery) -> T:
        ...
