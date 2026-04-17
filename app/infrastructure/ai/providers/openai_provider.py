from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

import logging

from app.common.config.settings import get_settings
from app.common.port.outbound.llm_port import LLMPort, LLMResponse

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMPort):
    """OpenAI LLM provider via LangChain."""

    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        settings = get_settings()
        self._model = model or settings.OPENAI_MODEL
        self._llm = ChatOpenAI(
            model=self._model,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=api_key or settings.OPENAI_API_KEY,
        )

    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        logger.debug(f"[OpenAI] Calling {self._model}, prompt_len={len(prompt)}")
        response = await self._llm.ainvoke(messages)

        usage = response.usage_metadata or {}
        return LLMResponse(
            content=str(response.content),
            model=self._model,
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
        )

    def get_model_name(self) -> str:
        return self._model

    def get_langchain_llm(self) -> ChatOpenAI:
        return self._llm
