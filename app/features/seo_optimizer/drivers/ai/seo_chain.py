"""
app/features/seo_optimizer/drivers/ai/seo_chain.py
─────────────────────────────────────────────────────────────
SEO analysis and optimization service.

Combines:
  1. textstat library — readability scores (no LLM needed)
  2. LangChain chain — AI-powered recommendations
  3. Rule-based analysis — keyword density, heading structure, etc.
"""

from __future__ import annotations
import re
import textstat

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.seo_optimizer.entities.seo_analysis import KeywordAnalysis, SEOAnalysis
from app.infrastructure.ai.llm_factory import get_llm_provider


class SEOAnalysisService:
    def __init__(self) -> None:
        self._llm = get_llm_provider().get_langchain_llm()

    def _analyze_keyword(self, content: str, keyword: str) -> KeywordAnalysis:
        if not keyword:
            return KeywordAnalysis()

        words = content.lower().split()
        keyword_lower = keyword.lower()
        occurrences = content.lower().count(keyword_lower)
        density = (occurrences / len(words) * 100) if words else 0.0

        paragraphs = content.split("\n\n")
        first_para = paragraphs[0].lower() if paragraphs else ""

        # Check headings (markdown)
        headings = re.findall(r"^#{1,6}\s+(.+)$", content, re.MULTILINE)
        in_headings = any(keyword_lower in h.lower() for h in headings)

        # Recommendation
        if density < 0.5:
            rec = f"Keyword '{keyword}' density ({density:.1f}%) is too low. Aim for 1-2%."
        elif density > 3.0:
            rec = f"Keyword '{keyword}' density ({density:.1f}%) is too high (keyword stuffing). Aim for 1-2%."
        else:
            rec = f"Keyword '{keyword}' density ({density:.1f}%) is optimal. ✅"

        return KeywordAnalysis(
            keyword=keyword,
            density_percent=round(density, 2),
            occurrences=occurrences,
            is_in_title=keyword_lower in content.split("\n")[0].lower() if content else False,
            is_in_first_paragraph=keyword_lower in first_para,
            is_in_headings=in_headings,
            recommendation=rec,
        )

    def _calculate_seo_score(self, analysis: SEOAnalysis) -> float:
        score = 0.0
        checks = [
            (analysis.word_count >= 600, 15, "Word count ≥ 600"),
            (analysis.has_h1, 10, "Has H1 heading"),
            (analysis.heading_count >= 3, 10, "Has ≥ 3 headings"),
            (analysis.flesch_reading_ease >= 50, 15, "Good readability"),
            (any(ka.density_percent >= 0.5 for ka in analysis.keyword_analyses), 15, "Keyword density ok"),
            (any(ka.is_in_headings for ka in analysis.keyword_analyses), 10, "Keyword in headings"),
            (analysis.internal_links_count >= 2, 10, "Internal links ≥ 2"),
            (analysis.images_with_alt == analysis.image_count, 5, "All images have alt text"),
            (analysis.meta_title_length in range(50, 61), 5, "Meta title 50-60 chars"),
            (analysis.meta_description_length in range(145, 161), 5, "Meta desc 145-160 chars"),
        ]

        for passed, weight, _ in checks:
            if passed:
                score += weight

        return round(score, 1)

    async def analyze(
        self,
        content: str,
        focus_keyword: str = "",
        meta_title: str = "",
        meta_description: str = "",
        url: str = "",
    ) -> SEOAnalysis:
        analysis = SEOAnalysis(
            content=content,
            url=url,
            focus_keyword=focus_keyword,
        )

        # ── Readability (textstat) ────────────────────────────────────────────
        analysis.flesch_reading_ease = textstat.flesch_reading_ease(content)
        analysis.flesch_kincaid_grade = textstat.flesch_kincaid_grade(content)
        analysis.avg_sentence_length = textstat.avg_sentence_length(content)
        analysis.word_count = len(content.split())

        # ── Heading analysis ──────────────────────────────────────────────────
        headings = re.findall(r"^(#{1,6})\s+(.+)$", content, re.MULTILINE)
        analysis.heading_count = len(headings)
        analysis.has_h1 = any(h[0] == "#" for h in headings)

        # ── Links ─────────────────────────────────────────────────────────────
        analysis.internal_links_count = len(re.findall(r"\[.*?\]\(/[^)]+\)", content))
        analysis.external_links_count = len(re.findall(r"\[.*?\]\(https?://[^)]+\)", content))

        # ── Images ────────────────────────────────────────────────────────────
        all_images = re.findall(r"!\[.*?\]\([^)]+\)", content)
        images_with_alt = re.findall(r"!\[.+?\]\([^)]+\)", content)
        analysis.image_count = len(all_images)
        analysis.images_with_alt = len(images_with_alt)

        # ── Meta ──────────────────────────────────────────────────────────────
        if meta_title:
            analysis.has_meta_title = True
            analysis.meta_title_length = len(meta_title)
        if meta_description:
            analysis.has_meta_description = True
            analysis.meta_description_length = len(meta_description)

        # ── Keyword analysis ──────────────────────────────────────────────────
        if focus_keyword:
            analysis.keyword_analyses = [self._analyze_keyword(content, focus_keyword)]

        # ── Score calculation ─────────────────────────────────────────────────
        analysis.seo_score = self._calculate_seo_score(analysis)
        analysis.readability_score = min(100, max(0, analysis.flesch_reading_ease))

        # ── AI recommendations ────────────────────────────────────────────────
        recs_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an SEO expert. Give 5 specific, actionable SEO improvement recommendations. Be concise."),
            ("human", (
                "Content stats:\n"
                f"- Word count: {analysis.word_count}\n"
                f"- SEO score: {analysis.seo_score}/100\n"
                f"- Readability (Flesch): {analysis.flesch_reading_ease:.1f}\n"
                f"- Focus keyword: {focus_keyword or 'not set'}\n"
                f"- Heading count: {analysis.heading_count}\n"
                f"- Internal links: {analysis.internal_links_count}\n"
                "List 5 specific improvements as bullet points."
            )),
        ])
        recs_chain = recs_prompt | self._llm | StrOutputParser()
        recs_raw = await recs_chain.ainvoke({})
        analysis.recommendations = [
            line.strip().lstrip("•-* ").strip()
            for line in recs_raw.split("\n")
            if line.strip() and len(line.strip()) > 10
        ][:5]

        return analysis
