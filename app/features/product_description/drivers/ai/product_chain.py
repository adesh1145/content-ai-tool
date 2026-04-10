"""
app/features/product_description/drivers/ai/product_chain.py
─────────────────────────────────────────────────────────────
LangChain chain for ecommerce product description generation.

Pattern: Feature → Benefit conversion (features tell, benefits sell).
"""

from __future__ import annotations
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.infrastructure.ai.llm_factory import get_llm_provider


class ProductDescAIService:
    def __init__(self) -> None:
        provider = get_llm_provider()
        from app.infrastructure.ai.llm_factory import OpenAIProvider, AnthropicProvider
        if isinstance(provider, (OpenAIProvider, AnthropicProvider)):
            self._llm = provider.get_langchain_llm()
        else:
            raise RuntimeError("Unsupported provider")

    async def generate(
        self,
        product_name: str,
        category: str,
        features: list[str],
        tone: str,
        target_audience: str,
        language: str,
        word_count: int = 150,
    ) -> dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert ecommerce copywriter. Convert product features into "
                "compelling benefits using the F-A-B (Feature-Advantage-Benefit) framework. "
                "Write descriptions that drive conversions. Use sensory language. "
                "Include a compelling opening line, key benefits, and a clear CTA."
            )),
            ("human", (
                "Product: {product_name}\n"
                "Category: {category}\n"
                "Features: {features}\n"
                "Tone: {tone}\n"
                "Target audience: {target_audience}\n"
                "Language: {language}\n"
                "Word count: approximately {word_count} words\n\n"
                "Write a compelling product description. Return the description text only."
            )),
        ])

        chain = prompt | self._llm | StrOutputParser()
        description = await chain.ainvoke({
            "product_name": product_name,
            "category": category,
            "features": "\n".join(f"- {f}" for f in features),
            "tone": tone,
            "target_audience": target_audience,
            "language": language,
            "word_count": word_count,
        })

        return {
            "description": description.strip(),
            "word_count": len(description.split()),
        }
