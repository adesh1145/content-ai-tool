"""
Driven adapter: LangChain multi-step blog generation pipeline.

Pipeline:
  1. Outline Generator  -> structured section headings
  2. Content Writer     -> full markdown blog body
  3. SEO Optimizer      -> meta title, description, slug
  4. Readability Check  -> Flesch-Kincaid score via textstat
"""

from __future__ import annotations

import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.blog_generator.domain.port.outbound.blog_ai_port import (
    BlogAIResult,
    IBlogAIService,
)
from app.features.blog_generator.domain.service.blog_domain_service import BlogDomainService
from app.infrastructure.ai.llm_registry import get_llm_registry


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


class BlogAIService(IBlogAIService):
    """
    Implements IBlogAIService using a multi-step LangChain pipeline.
    Uses the LLM registry to obtain the underlying language model.
    """

    def __init__(self, provider: str = "openai", model: str | None = None) -> None:
        llm_provider = get_llm_registry().get_provider(provider, model)
        self._llm = llm_provider.get_langchain_llm()

    async def generate_blog(
        self,
        *,
        topic: str,
        tone: str,
        language: str,
        target_audience: str,
        focus_keyword: str,
        secondary_keywords: list[str],
        word_count: int,
    ) -> BlogAIResult:
        outline = await self._generate_outline(
            topic, focus_keyword, tone, target_audience, word_count
        )
        body = await self._write_body(
            topic, focus_keyword, secondary_keywords, tone, language,
            target_audience, word_count, outline,
        )
        seo_data = await self._generate_seo(topic, focus_keyword, body)

        readability = BlogDomainService.calculate_readability_score(body)
        actual_word_count = len(body.split())
        reading_time = BlogDomainService.calculate_reading_time(actual_word_count)
        tokens_used = self._estimate_tokens(body, outline)

        return BlogAIResult(
            title=seo_data.get("title", f"{topic[:55]} — Complete Guide"),
            body=body,
            outline=outline,
            meta_title=seo_data.get("title", f"{topic[:55]} — Complete Guide"),
            meta_description=seo_data.get(
                "meta_description", f"Learn everything about {topic}."
            ),
            slug=seo_data.get("slug", _slugify(topic)),
            focus_keyword=focus_keyword or topic,
            secondary_keywords=secondary_keywords,
            word_count=actual_word_count,
            readability_score=readability,
            reading_time_minutes=reading_time,
            tokens_used=tokens_used,
        )

    async def _generate_outline(
        self, topic: str, focus_keyword: str, tone: str,
        target_audience: str, word_count: int,
    ) -> list[str]:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an expert SEO content strategist. Create a structured blog outline "
             "optimised for both readers and search engines. Return ONLY a JSON array of "
             "section headings (strings). No extra text."),
            ("human",
             "Blog topic: {topic}\nFocus keyword: {focus_keyword}\nTone: {tone}\n"
             "Target audience: {target_audience}\nWord count target: {word_count} words\n\n"
             'Return a JSON array like: ["Introduction", "Section 1", ...]'),
        ])
        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "topic": topic,
            "focus_keyword": focus_keyword or topic,
            "tone": tone,
            "target_audience": target_audience,
            "word_count": word_count,
        })
        try:
            return json.loads(raw.strip())
        except json.JSONDecodeError:
            return [line.strip() for line in raw.split("\n") if line.strip()]

    async def _write_body(
        self, topic: str, focus_keyword: str, secondary_keywords: list[str],
        tone: str, language: str, target_audience: str,
        word_count: int, outline: list[str],
    ) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are a professional content writer specialising in SEO-optimised blog posts. "
             "Write engaging, well-structured markdown content. Naturally incorporate the focus "
             "keyword and secondary keywords. Use proper H2/H3 headings, short paragraphs, "
             "bullet points where appropriate. Don't stuff keywords."),
            ("human",
             "Write a complete {word_count}-word blog post in {language} with {tone} tone.\n"
             "Topic: {topic}\nFocus keyword: {focus_keyword}\n"
             "Secondary keywords: {secondary_keywords}\n"
             "Target audience: {target_audience}\nOutline to follow:\n{outline}\n\n"
             "Return only the blog post in markdown format."),
        ])
        chain = prompt | self._llm | StrOutputParser()
        return await chain.ainvoke({
            "topic": topic,
            "focus_keyword": focus_keyword or topic,
            "secondary_keywords": ", ".join(secondary_keywords) or "none",
            "tone": tone,
            "language": language,
            "target_audience": target_audience,
            "word_count": word_count,
            "outline": "\n".join(f"- {h}" for h in outline),
        })

    async def _generate_seo(self, topic: str, focus_keyword: str, body: str) -> dict:
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an SEO specialist. Generate precise, click-worthy SEO metadata. "
             "Return ONLY a valid JSON object with these exact keys: "
             "title (50-60 chars), meta_description (145-160 chars), slug (URL-friendly)."),
            ("human",
             "Blog content summary:\nTopic: {topic}\nFocus keyword: {focus_keyword}\n"
             "First 200 chars of body: {body_preview}\n\n"
             'Return JSON: {{"title": "...", "meta_description": "...", "slug": "..."}}'),
        ])
        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "topic": topic,
            "focus_keyword": focus_keyword or topic,
            "body_preview": body[:200],
        })
        try:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                return json.loads(match.group())
        except (json.JSONDecodeError, AttributeError):
            pass
        return {}

    @staticmethod
    def _estimate_tokens(body: str, outline: list[str]) -> int:
        try:
            import tiktoken  # noqa: PLC0415
            enc = tiktoken.encoding_for_model("gpt-4o-mini")
            return len(enc.encode(body)) + len(enc.encode(str(outline)))
        except Exception:
            return len(body.split()) * 2
