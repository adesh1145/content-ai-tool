"""
app/features/script_writer/drivers/ai/script_chain.py
─────────────────────────────────────────────────────────────
LangChain chain for video/audio script writing.

Formats:
  - YouTube: Hook (0-30s) + Body sections + CTA + Like/Subscribe
  - Reel: Ultra-short (15-60s), high-impact hook + value + CTA
  - Podcast: Conversational intro + talking points + outro
"""

from __future__ import annotations
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.infrastructure.ai.llm_factory import get_llm_provider
from app.features.script_writer.use_cases.interfaces.script_interfaces import IScriptAIService


SCRIPT_SYSTEM_PROMPTS = {
    "youtube": (
        "You are a YouTube script writer. Structure scripts with:\n"
        "1. HOOK (0-30 seconds) — grab attention immediately\n"
        "2. INTRO — who you are and what video covers\n"
        "3. MAIN CONTENT — 3-5 key sections with timestamps\n"
        "4. CTA — subscribe, like, comment ask\n"
        "Use conversational language. Add [PAUSE], [B-ROLL], [GRAPHIC] cues where needed."
    ),
    "reel": (
        "You are a viral short-form video script writer (Instagram Reels/TikTok). "
        "Scripts must be 15-60 seconds when spoken at normal pace. "
        "Structure: HOOK (1-2 sentences that stop the scroll) → VALUE (main point) → CTA. "
        "Be punchy, use pattern interrupts, speak directly to camera."
    ),
    "podcast": (
        "You are a podcast script writer. Create a conversational, engaging script with:\n"
        "1. INTRO — catchy opening + episode preview\n"
        "2. TOPIC SEGMENTS — natural talking points (not word-for-word, bullet style)\n"
        "3. KEY INSIGHTS — main takeaways\n"
        "4. OUTRO — recap + next episode teaser + CTA\n"
        "Tone is natural and conversational, like a real conversation."
    ),
}


class ScriptAIService(IScriptAIService):
    def __init__(self) -> None:
        self._llm = get_llm_provider().get_langchain_llm()

    async def generate(
        self,
        script_format: str,
        topic: str,
        tone: str,
        language: str,
        target_audience: str,
        duration_seconds: int = 300,
    ) -> dict:
        system = SCRIPT_SYSTEM_PROMPTS.get(script_format, SCRIPT_SYSTEM_PROMPTS["youtube"])

        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", (
                "Topic: {topic}\n"
                "Tone: {tone}\n"
                "Language: {language}\n"
                "Target audience: {target_audience}\n"
                "Target duration: {duration} seconds\n\n"
                "Write the complete {format} script now."
            )),
        ])

        chain = prompt | self._llm | StrOutputParser()
        script = await chain.ainvoke({
            "topic": topic,
            "tone": tone,
            "language": language,
            "target_audience": target_audience,
            "duration": duration_seconds,
            "format": script_format,
        })

        # Estimate spoken words: ~130 words/min
        estimated_duration = int((len(script.split()) / 130) * 60)

        return {
            "script": script.strip(),
            "word_count": len(script.split()),
            "estimated_duration_seconds": estimated_duration,
        }
