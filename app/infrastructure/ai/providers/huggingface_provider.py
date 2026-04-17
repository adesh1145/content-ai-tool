from __future__ import annotations

import logging

from app.common.config.settings import get_settings
from app.common.port.outbound.llm_port import LLMPort, LLMResponse

logger = logging.getLogger(__name__)


class HuggingFaceProvider(LLMPort):
    """HuggingFace LLM provider via langchain-huggingface."""

    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        try:
            from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
        except ImportError as e:
            raise ImportError("Install langchain-huggingface: pip install langchain-huggingface") from e

        settings = get_settings()
        self._model = model or getattr(settings, "HUGGINGFACE_MODEL", "mistralai/Mistral-7B")
        endpoint = HuggingFaceEndpoint(
            repo_id=self._model,
            huggingfacehub_api_token=api_key or getattr(settings, "HUGGINGFACE_API_KEY", ""),
            temperature=settings.LLM_TEMPERATURE,
            max_new_tokens=settings.LLM_MAX_TOKENS,
        )
        self._llm = ChatHuggingFace(llm=endpoint)

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

        logger.debug(f"[HuggingFace] Calling {self._model}, prompt_len={len(prompt)}")
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
