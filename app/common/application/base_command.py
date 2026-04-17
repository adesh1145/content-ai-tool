from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class BaseCommand(BaseModel):
    """Marker base for all commands (input DTOs for write operations)."""
    pass


class CommandHandler(ABC, Generic[T]):
    @abstractmethod
    async def handle(self, command: BaseCommand) -> T:
        ...
