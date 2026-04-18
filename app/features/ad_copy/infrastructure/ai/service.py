"""
Driven adapter: LangChain ad copy generation using platform-specific prompts.
Uses the LLM configured in AD_COPY_LLM from model_config.py.

Google Ads  -> AIDA framework (Attention-Interest-Desire-Action), headline <=30 chars
Facebook Ads -> PAS framework (Problem-Agitate-Solution), emotionally compelling
"""

from __future__ import annotations

import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.ad_copy.domain.port.outbound.ad_ai_port import AdAIPort
from app.infrastructure.ai.llm_registry import get_llm_registry
from app.infrastructure.ai.model_config import AD_COPY_LLM

_GOOGLE_SYSTEM = (
    "You are a Google Ads specialist using the AIDA framework "
    "(Attention-Interest-Desire-Action). "
    "Headlines MUST be <=30 characters. Descriptions MUST be <=90 characters. "
    "Return a JSON object with keys: headline, primary_text, cta_text, variations. "
    "variations is an array of {num_variations} objects each with headline, primary_text, cta_text. "
    "Return ONLY valid JSON, no other text."
)

_FACEBOOK_SYSTEM = (
    "You are a Facebook Ads expert using the PAS framework "
    "(Problem-Agitate-Solution). "
    "Write emotionally compelling copy that drives action. "
    "Return a JSON object with keys: headline, primary_text, cta_text, variations. "
    "variations is an array of {num_variations} objects each with headline, primary_text, cta_text. "
    "Return ONLY valid JSON, no other text."
)

_HUMAN_PROMPT = (
    "Product: {product_name}\n"
    "Description: {product_description}\n"
    "Target audience: {target_audience}\n"
    "Tone: {tone}\n"
    "Language: {language}\n\n"
    "Generate a primary ad copy plus {num_variations} A/B test variations."
)


class AdCopyAIService(AdAIPort):
    """Implements AdAIPort. Model from model_config.py."""

    def __init__(self) -> None:
        step = AD_COPY_LLM.get_step("generate")
        self._llm = get_llm_registry().get_langchain_llm(step.provider, step.model)

    async def generate(
        self,
        platform: str,
        product_name: str,
        product_description: str,
        target_audience: str,
        tone: str,
        language: str,
        num_variations: int = 2,
    ) -> dict:
        system_prompt = _GOOGLE_SYSTEM if platform == "google" else _FACEBOOK_SYSTEM

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", _HUMAN_PROMPT),
        ])

        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "product_name": product_name,
            "product_description": product_description,
            "target_audience": target_audience,
            "tone": tone,
            "language": language,
            "num_variations": num_variations,
        })

        return self._parse_response(raw, product_name)

    @staticmethod
    def _parse_response(raw: str, fallback_product: str) -> dict:
        try:
            json_match = re.search(r"\{.*\}", raw, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "headline": data.get("headline", fallback_product),
                    "primary_text": data.get("primary_text", ""),
                    "cta_text": data.get("cta_text", "Learn More"),
                    "variations": data.get("variations", []),
                    "tokens_used": len(raw.split()) * 2,
                }
        except (json.JSONDecodeError, AttributeError):
            pass
        return {
            "headline": fallback_product,
            "primary_text": raw[:200],
            "cta_text": "Learn More",
            "variations": [],
            "tokens_used": len(raw.split()) * 2,
        }
