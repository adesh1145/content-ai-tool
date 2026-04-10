"""
app/features/blog_generator/drivers/ai/blog_chain.py
─────────────────────────────────────────────────────────────
LangChain blog generation chain.
Layer 4: Frameworks & Drivers — concrete AI implementation.

Pipeline:
  1. Outline Generator  → structured section headings
  2. Content Writer     → full markdown blog body for each section
  3. SEO Optimizer      → meta title, meta desc, slug, schema markup
  4. Readability Check  → Flesch-Kincaid score via textstat
"""

from __future__ import annotations

import re
import json
import textstat

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.blog_generator.entities.blog_content import SEOMetadata
from app.features.blog_generator.use_cases.interfaces.blog_interfaces import (
    BlogGenerationRequest,
    BlogGenerationResult,
    IBlogAIService,
)
from app.infrastructure.ai.llm_factory import get_llm_provider


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text)


class BlogAIService(IBlogAIService):
    """
    Implements IBlogAIService using a multi-step LangChain pipeline.
    Injected into GenerateBlogUseCase via constructor DI.
    """

    def __init__(self) -> None:
        provider = get_llm_provider()
        # Access raw LangChain LLM from our provider
        from app.infrastructure.ai.llm_factory import OpenAIProvider, AnthropicProvider
        if isinstance(provider, (OpenAIProvider, AnthropicProvider)):
            self._llm = provider.get_langchain_llm()
        else:
            raise RuntimeError("Unsupported provider type for chain building.")

    async def generate(self, request: BlogGenerationRequest) -> BlogGenerationResult:
        # ── Step 1: Generate Outline ──────────────────────────────────────────
        outline_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert SEO content strategist. Create a structured blog outline "
                "optimised for both readers and search engines. Return ONLY a JSON array of "
                "section headings (strings). No extra text."
            )),
            ("human", (
                "Blog topic: {topic}\n"
                "Focus keyword: {focus_keyword}\n"
                "Tone: {tone}\n"
                "Target audience: {target_audience}\n"
                "Word count target: {word_count} words\n\n"
                "Return a JSON array like: [\"Introduction\", \"Section 1\", ...]"
            )),
        ])
        outline_chain = outline_prompt | self._llm | StrOutputParser()
        outline_raw = await outline_chain.ainvoke({
            "topic": request.topic,
            "focus_keyword": request.focus_keyword or request.topic,
            "tone": request.tone,
            "target_audience": request.target_audience,
            "word_count": request.word_count,
        })

        try:
            outline: list[str] = json.loads(outline_raw.strip())
        except json.JSONDecodeError:
            # Fallback: extract lines
            outline = [line.strip() for line in outline_raw.split("\n") if line.strip()]

        # ── Step 2: Write Blog Body ───────────────────────────────────────────
        body_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are a professional content writer specialising in SEO-optimised blog posts. "
                "Write engaging, well-structured markdown content. Naturally incorporate the focus "
                "keyword and secondary keywords. Use proper H2/H3 headings, short paragraphs, "
                "bullet points where appropriate. Don't stuff keywords."
            )),
            ("human", (
                "Write a complete {word_count}-word blog post in {language} with {tone} tone.\n"
                "Topic: {topic}\n"
                "Focus keyword: {focus_keyword}\n"
                "Secondary keywords: {secondary_keywords}\n"
                "Target audience: {target_audience}\n"
                "Outline to follow:\n{outline}\n\n"
                "Return only the blog post in markdown format."
            )),
        ])
        body_chain = body_prompt | self._llm | StrOutputParser()
        body = await body_chain.ainvoke({
            "topic": request.topic,
            "focus_keyword": request.focus_keyword or request.topic,
            "secondary_keywords": ", ".join(request.secondary_keywords) or "none",
            "tone": request.tone,
            "language": request.language,
            "target_audience": request.target_audience,
            "word_count": request.word_count,
            "outline": "\n".join(f"- {h}" for h in outline),
        })

        # ── Step 3: Generate SEO Metadata ─────────────────────────────────────
        seo_prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an SEO specialist. Generate precise, click-worthy SEO metadata. "
                "Return ONLY a valid JSON object with these exact keys: "
                "title (50-60 chars), meta_description (145-160 chars), slug (URL-friendly)."
            )),
            ("human", (
                "Blog content summary:\nTopic: {topic}\nFocus keyword: {focus_keyword}\n"
                "First 200 chars of body: {body_preview}\n\n"
                "Return JSON: {{\"title\": \"...\", \"meta_description\": \"...\", \"slug\": \"...\"}}"
            )),
        ])
        seo_chain = seo_prompt | self._llm | StrOutputParser()
        seo_raw = await seo_chain.ainvoke({
            "topic": request.topic,
            "focus_keyword": request.focus_keyword or request.topic,
            "body_preview": body[:200],
        })

        seo_data: dict = {}
        try:
            # Extract JSON from response
            json_match = re.search(r"\{.*\}", seo_raw, re.DOTALL)
            if json_match:
                seo_data = json.loads(json_match.group())
        except (json.JSONDecodeError, AttributeError):
            pass

        # ── Step 4: Readability Score ──────────────────────────────────────────
        readability = textstat.flesch_reading_ease(body)
        word_count = len(body.split())

        seo = SEOMetadata(
            meta_title=seo_data.get("title", f"{request.topic[:55]} — Complete Guide"),
            meta_description=seo_data.get("meta_description", f"Learn everything about {request.topic}."),
            slug=seo_data.get("slug", _slugify(request.topic)),
            focus_keyword=request.focus_keyword or request.topic,
            secondary_keywords=request.secondary_keywords,
            reading_time_minutes=max(1, word_count // 200),
            word_count=word_count,
            readability_score=readability,
        )

        # ── Estimate tokens ───────────────────────────────────────────────────
        import tiktoken
        try:
            enc = tiktoken.encoding_for_model("gpt-4o-mini")
            tokens_used = len(enc.encode(body)) + len(enc.encode(str(outline)))
        except Exception:
            tokens_used = word_count * 2  # rough estimate

        return BlogGenerationResult(
            title=seo.meta_title,
            outline=outline,
            body=body,
            seo=seo,
            tokens_used=tokens_used,
        )
