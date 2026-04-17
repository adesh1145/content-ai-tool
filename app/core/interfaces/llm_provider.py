"""
app/core/interfaces/llm_provider.py
─────────────────────────────────────────────────────────────
Abstract LLM provider interface (DIP).

Use cases and AI services depend on this interface,
NEVER on OpenAI or Anthropic SDKs directly.
Swap providers by changing only llm_factory.py.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Structured response from any LLM provider."""
    content: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ILLMProvider(ABC):
    """
    Abstract LLM provider.

    Concrete implementations:
      - OpenAIProvider  (app/infrastructure/ai/llm_factory.py)
      - AnthropicProvider (app/infrastructure/ai/llm_factory.py)
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        """Generate a single text response from the LLM."""
        ...

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the model identifier string."""
        ...

    @abstractmethod
    def get_langchain_llm(self):
        """
        Return the underlying LangChain BaseChatModel instance.

        Used by AI service implementations (drivers/ai/) to build
        LangChain chains and LangGraph graphs. This is scoped to
        Layer 4 only — use cases must NEVER call this.
        """
        ...
