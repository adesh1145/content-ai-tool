"""
Driven adapter: LangChain product description generation using F-A-B framework.

F-A-B = Feature-Advantage-Benefit
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.product_description.domain.port.outbound.product_ai_port import ProductAIPort
from app.features.product_description.domain.service.fab_framework_service import FABFrameworkService
from app.infrastructure.ai.llm_registry import get_llm_registry

_SYSTEM_PROMPT = (
    "You are a world-class product copywriter. "
    "Use the F-A-B (Feature-Advantage-Benefit) framework to craft compelling "
    "product descriptions that convert browsers into buyers. "
    "Return ONLY the product description text, no explanations or formatting markers."
)


class ProductAIService(ProductAIPort):
    """
    Implements ProductAIPort using LangChain with F-A-B framework prompts.
    """

    def __init__(self, provider: str = "openai", model: str | None = None) -> None:
        llm_provider = get_llm_registry().get_provider(provider, model)
        self._llm = llm_provider.get_langchain_llm()

    async def generate(
        self,
        product_name: str,
        category: str,
        features: list[str],
        tone: str,
        target_audience: str,
        language: str,
        word_count: int,
    ) -> dict:
        fab_prompt = FABFrameworkService.build_fab_prompt(
            product_name=product_name,
            category=category,
            features=features,
            tone=tone,
            target_audience=target_audience,
            word_count=word_count,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", _SYSTEM_PROMPT),
            ("human", "{fab_prompt}\n\nLanguage: {language}"),
        ])

        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "fab_prompt": fab_prompt,
            "language": language,
        })

        return {
            "description": raw.strip(),
            "tokens_used": len(raw.split()) * 2,
        }
