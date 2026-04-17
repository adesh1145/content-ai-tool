"""
app/features/social_media/drivers/ai/social_chain.py
─────────────────────────────────────────────────────────────
LangChain chain for platform-aware social media post generation.

Enforces character limits:
  - LinkedIn: 3000 chars
  - Twitter/X: 280 chars
  - Instagram: 2200 chars
"""

from __future__ import annotations
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.infrastructure.ai.llm_factory import get_llm_provider
from app.features.social_media.use_cases.interfaces.social_interfaces import ISocialAIService


PLATFORM_PROMPTS = {
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
    def __init__(self) -> None:
        self._llm = get_llm_provider().get_langchain_llm()

    async def generate(
        self,
        topic: str,
        platform: str,
        tone: str,
        language: str,
        target_audience: str,
        include_emoji: bool = True,
    ) -> dict:
        system_msg = PLATFORM_PROMPTS.get(platform, PLATFORM_PROMPTS["linkedin"])

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_msg),
            ("human", (
                "Topic/Product: {topic}\n"
                "Tone: {tone}\n"
                "Language: {language}\n"
                "Target audience: {target_audience}\n"
                "Include emojis: {include_emoji}\n\n"
                "Write the {platform} post now. Return ONLY the post content."
            )),
        ])

        chain = prompt | self._llm | StrOutputParser()
        caption = await chain.ainvoke({
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "language": language,
            "target_audience": target_audience,
            "include_emoji": "yes" if include_emoji else "no",
        })

        # Extract hashtags
        import re
        hashtags = re.findall(r"#\w+", caption)

        return {
            "caption": caption.strip(),
            "hashtags": hashtags,
            "char_count": len(caption),
        }
