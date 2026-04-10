"""
app/features/ad_copy/drivers/ai/ad_chain.py
─────────────────────────────────────────────────────────────
LangChain ad copy generation chain.

Google Ads: AIDA framework, headline ≤30 chars, description ≤90 chars
Facebook Ads: PAS framework (Problem-Agitate-Solution), more creative
"""

from __future__ import annotations
import json, re
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.infrastructure.ai.llm_factory import get_llm_provider


class AdCopyAIService:
    def __init__(self) -> None:
        provider = get_llm_provider()
        from app.infrastructure.ai.llm_factory import OpenAIProvider, AnthropicProvider
        if isinstance(provider, (OpenAIProvider, AnthropicProvider)):
            self._llm = provider.get_langchain_llm()
        else:
            raise RuntimeError("Unsupported provider")

    async def generate(
        self,
        platform: str,
        product: str,
        target_audience: str,
        usp: str,
        tone: str,
        num_variations: int = 3,
    ) -> list[dict]:

        if platform == "google":
            system = (
                "You are a Google Ads specialist. Use the AIDA framework. "
                "Headlines MUST be ≤30 characters each. Descriptions MUST be ≤90 characters. "
                f"Generate {num_variations} ad variations as a JSON array with keys: "
                "headline, body, cta. Return ONLY valid JSON array, no other text."
            )
        else:  # facebook
            system = (
                "You are a Facebook Ads expert. Use the PAS framework (Problem-Agitate-Solution). "
                "Write emotionally compelling copy that drives action. "
                f"Generate {num_variations} ad variations as a JSON array with keys: "
                "headline, body, cta. Return ONLY valid JSON array, no other text."
            )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", (
                "Product/Service: {product}\n"
                "Target audience: {target_audience}\n"
                "Unique selling point: {usp}\n"
                "Tone: {tone}\n\n"
                "Generate {num_variations} high-converting ad variations."
            )),
        ])

        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "product": product,
            "target_audience": target_audience,
            "usp": usp,
            "tone": tone,
            "num_variations": num_variations,
        })

        try:
            json_match = re.search(r"\[.*\]", raw, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except (json.JSONDecodeError, AttributeError):
            pass

        return [{"headline": product, "body": raw[:90], "cta": "Learn More"}]
