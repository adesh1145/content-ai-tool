from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class RepositoryPort(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> T:
        ...

    @abstractmethod
    async def find_by_id(self, id: str) -> T | None:
        ...

    @abstractmethod
    async def find_all(self, *, skip: int = 0, limit: int = 100) -> list[T]:
        ...

    @abstractmethod
    async def delete(self, id: str) -> bool:
        ...
