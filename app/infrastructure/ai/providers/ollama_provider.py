"""
Ollama local LLM provider — requires explicit model name.

Usage:
    provider = OllamaProvider(model="llama3")
    provider = OllamaProvider(model="mistral")
    provider = OllamaProvider(model="codellama")
"""

from __future__ import annotations

import logging

from app.common.config.settings import get_settings
from app.common.port.outbound.llm_port import LLMPort, LLMResponse

logger = logging.getLogger(__name__)


class OllamaProvider(LLMPort):
    """Ollama local LLM provider via langchain-ollama. Model MUST be specified."""

    def __init__(self, model: str, base_url: str | None = None) -> None:
        try:
            from langchain_ollama import ChatOllama
        except ImportError as e:
            raise ImportError(
                "Install langchain-ollama: pip install langchain-ollama"
            ) from e

        settings = get_settings()
        self._model = model
        self._llm = ChatOllama(
            model=self._model,
            base_url=base_url or settings.OLLAMA_BASE_URL,
            temperature=settings.LLM_TEMPERATURE,
        )

    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        from langchain_core.messages import HumanMessage, SystemMessage

        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        logger.debug("[Ollama] Calling %s, prompt_len=%d", self._model, len(prompt))
        response = await self._llm.ainvoke(messages)

        return LLMResponse(
            content=str(response.content),
            model=self._model,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
        )

    def get_model_name(self) -> str:
        return self._model

    def get_langchain_llm(self):
        return self._llm
