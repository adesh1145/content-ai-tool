"""
Driven adapter: social media content generation.
Uses the LLM configured in SOCIAL_MEDIA_LLM from model_config.py.
"""

from __future__ import annotations

import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.social_media.domain.port.outbound.social_ai_port import (
    ISocialAIService,
    SocialAIResult,
)
from app.infrastructure.ai.llm_registry import get_llm_registry
from app.infrastructure.ai.model_config import SOCIAL_MEDIA_LLM

PLATFORM_PROMPTS: dict[str, str] = {
    "linkedin": (
        "You are a LinkedIn content expert. Write a professional, value-driven post "
        "that sparks engagement. Include a hook in the first line, 3-5 key insights, "
        "and a question or CTA at the end. Use line breaks for readability. "
        "Max 3000 characters. Include 3-5 relevant hashtags at the end."
    ),
    "twitter": (
        "You are a viral Twitter/X content creator. Write a punchy, attention-grabbing tweet "
        "or thread opener. Be concise, witty, and direct. STRICTLY under 280 characters "
        "(not including hashtags). Include 1-2 hashtags."
    ),
    "instagram": (
        "You are an Instagram content strategist. Write an engaging caption that tells "
        "a story or shares value. Start with a hook. Use emojis naturally. End with a "
        "CTA. Include 5-10 relevant hashtags. Max 2200 characters."
    ),
}


class SocialAIService(ISocialAIService):
    """Driven adapter — generates social-media content. Model from model_config.py."""

    def __init__(self) -> None:
        step = SOCIAL_MEDIA_LLM.get_step("generate")
        self._llm = get_llm_registry().get_langchain_llm(step.provider, step.model)

    async def generate(
        self,
        *,
        topic: str,
        platform: str,
        tone: str,
        language: str,
        target_audience: str,
    ) -> SocialAIResult:
        system_msg = PLATFORM_PROMPTS.get(
            platform.lower(), PLATFORM_PROMPTS["linkedin"]
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_msg),
            (
                "human",
                "Topic/Product: {topic}\n"
                "Tone: {tone}\n"
                "Language: {language}\n"
                "Target audience: {target_audience}\n\n"
                "Write the {platform} post now. Return ONLY the post content.",
            ),
        ])

        chain = prompt | self._llm | StrOutputParser()
        caption: str = await chain.ainvoke({
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "language": language,
            "target_audience": target_audience,
        })

        hashtags: list[str] = re.findall(r"#\w+", caption)

        return SocialAIResult(
            content=caption.strip(),
            hashtags=hashtags,
            char_count=len(caption.strip()),
        )
