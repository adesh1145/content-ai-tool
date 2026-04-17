from __future__ import annotations

import logging

from app.common.config.settings import get_settings
from app.common.port.outbound.llm_port import LLMPort, LLMResponse

logger = logging.getLogger(__name__)


class OllamaProvider(LLMPort):
    """Ollama local LLM provider via langchain-ollama."""

    def __init__(self, model: str | None = None, base_url: str | None = None) -> None:
        try:
            from langchain_ollama import ChatOllama
        except ImportError as e:
            raise ImportError("Install langchain-ollama: pip install langchain-ollama") from e

        settings = get_settings()
        self._model = model or getattr(settings, "OLLAMA_MODEL", "llama3")
        self._llm = ChatOllama(
            model=self._model,
            base_url=base_url or getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434"),
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

        logger.debug(f"[Ollama] Calling {self._model}, prompt_len={len(prompt)}")
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
