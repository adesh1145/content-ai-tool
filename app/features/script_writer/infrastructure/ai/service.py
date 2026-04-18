"""
Driven adapter: LangChain script generation with format-specific prompts.

YouTube  → Hook (0-30s) + Intro + Main Content (3-5 sections with timestamps) + CTA
Reel     → 15-60s, HOOK -> VALUE -> CTA. Punchy, pattern interrupts
Podcast  → INTRO + TOPIC SEGMENTS (bullet-style talking points) + KEY INSIGHTS + OUTRO
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.script_writer.domain.port.outbound.script_ai_port import (
    IScriptAIService,
    ScriptAIResult,
)
from app.features.script_writer.domain.service.script_domain_service import ScriptDomainService
from app.infrastructure.ai.llm_registry import get_llm_registry

_YOUTUBE_SYSTEM = (
    "You are a YouTube scriptwriter. Write a script with this structure:\n"
    "1. HOOK (0-30 seconds) — Grab attention immediately\n"
    "2. INTRO — Set up what the video covers\n"
    "3. MAIN CONTENT — 3-5 sections, each with [TIMESTAMP] markers\n"
    "4. CTA — Call to action (subscribe, comment, etc.)\n\n"
    "Include production cues: [PAUSE], [B-ROLL], [GRAPHIC], [CUT TO].\n"
    "Target duration: {duration_seconds} seconds (~{word_target} words at 130 wpm).\n"
    "Tone: {tone}. Language: {language}."
)

_REEL_SYSTEM = (
    "You are a short-form video scriptwriter (Reels / Shorts / TikTok).\n"
    "Duration: 15-60 seconds. Structure:\n"
    "1. HOOK (first 3 seconds) — Pattern interrupt, bold statement\n"
    "2. VALUE — Core message, fast pacing, punchy lines\n"
    "3. CTA — Clear call to action\n\n"
    "Keep sentences short. Use line breaks for pacing.\n"
    "Target duration: {duration_seconds} seconds (~{word_target} words).\n"
    "Tone: {tone}. Language: {language}."
)

_PODCAST_SYSTEM = (
    "You are a podcast scriptwriter. Write a conversational script with:\n"
    "1. INTRO — Welcome, episode topic, why it matters\n"
    "2. TOPIC SEGMENTS — 3-5 segments with bullet-style talking points\n"
    "3. KEY INSIGHTS — Top 3 takeaways\n"
    "4. OUTRO — Recap, next episode tease, where to follow\n\n"
    "Use a natural, conversational style. Include [MUSIC CUE] and [AD BREAK] markers.\n"
    "Target duration: {duration_seconds} seconds (~{word_target} words at 130 wpm).\n"
    "Tone: {tone}. Language: {language}."
)

_HUMAN_PROMPT = (
    "Topic: {topic}\n"
    "Target audience: {target_audience}\n\n"
    "Write the complete script."
)

_FORMAT_PROMPTS = {
    "youtube": _YOUTUBE_SYSTEM,
    "reel": _REEL_SYSTEM,
    "podcast": _PODCAST_SYSTEM,
}


class ScriptAIService(IScriptAIService):
    """Implements IScriptAIService using LangChain with the LLM registry."""

    def __init__(self, provider: str | None = None, model: str | None = None) -> None:
        llm_provider = get_llm_registry().get_provider(provider, model)
        self._llm = llm_provider.get_langchain_llm()

    async def generate_script(
        self,
        *,
        script_format: str,
        topic: str,
        tone: str,
        language: str,
        target_audience: str,
        duration_seconds: int,
    ) -> ScriptAIResult:
        wpm = 130
        word_target = round((duration_seconds / 60) * wpm)

        system_template = _FORMAT_PROMPTS.get(script_format, _YOUTUBE_SYSTEM)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", _HUMAN_PROMPT),
        ])

        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "topic": topic,
            "tone": tone,
            "language": language,
            "target_audience": target_audience or "general audience",
            "duration_seconds": duration_seconds,
            "word_target": word_target,
        })

        word_count = len(raw.split())
        estimated_duration = ScriptDomainService.estimate_spoken_duration(word_count, wpm)

        return ScriptAIResult(
            script_text=raw,
            word_count=word_count,
            estimated_duration_seconds=estimated_duration,
        )
