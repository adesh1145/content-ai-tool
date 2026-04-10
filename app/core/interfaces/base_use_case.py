"""
app/core/interfaces/base_use_case.py
─────────────────────────────────────────────────────────────
Abstract use case contract (SRP + OCP).

Every use case in the system implements this interface, 
making them uniform, mockable, and independently testable.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class IUseCase(ABC, Generic[InputT, OutputT]):
    """
    Base use case interface.

    SOLID:
      - SRP: One use case = one application action.
      - OCP: New behaviour → new use case class, no modification.
    """

    @abstractmethod
    async def execute(self, input_data: InputT) -> OutputT:
        """Execute the use case and return its output."""
        ...
