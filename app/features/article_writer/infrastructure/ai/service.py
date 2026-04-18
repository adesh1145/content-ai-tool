"""
Driven adapter: LangGraph 5-step article generation pipeline.

MULTI-LLM DESIGN — each step uses a different LLM:
  1. research  → configured LLM (e.g. GPT-4o for broad reasoning)
  2. outline   → configured LLM
  3. draft     → configured LLM (e.g. Claude for prose quality)
  4. edit      → configured LLM (e.g. Claude for editing)
  5. finalize  → configured LLM (e.g. GPT-4o-mini for SEO metadata)

Change models in model_config.py without touching this code.
"""

from __future__ import annotations

import json
import re
from typing import TypedDict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, StateGraph

from app.features.article_writer.domain.port.outbound.article_ai_port import (
    ArticleAIResult,
    IArticleAIService,
)
from app.infrastructure.ai.llm_registry import get_llm_registry
from app.infrastructure.ai.model_config import ARTICLE_WRITER_LLM


class _ArticleGraphState(TypedDict):
    topic: str
    tone: str
    language: str
    target_audience: str
    focus_keyword: str
    word_count: int
    research: str
    outline: str
    draft: str
    edited_draft: str
    final_article: str
    meta_title: str
    meta_description: str


def _get_step_llm(step_name: str):
    """Get the LangChain LLM for a specific article pipeline step."""
    step = ARTICLE_WRITER_LLM.get_step(step_name)
    return get_llm_registry().get_langchain_llm(step.provider, step.model)


async def _research_node(state: _ArticleGraphState) -> _ArticleGraphState:
    llm = _get_step_llm("research")
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a research assistant. Identify the most important angles, "
         "facts, statistics, and expert perspectives for the given topic."),
        ("human",
         "Topic: {topic}\nAudience: {target_audience}\nKeyword: {focus_keyword}\n\n"
         "List 5-7 key research points, facts, and angles. Be specific."),
    ])
    chain = prompt | llm | StrOutputParser()
    research = await chain.ainvoke(state)
    return {**state, "research": research}


async def _outline_node(state: _ArticleGraphState) -> _ArticleGraphState:
    llm = _get_step_llm("outline")
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a content strategist. Create a detailed article outline "
         "optimised for SEO and reader engagement."),
        ("human",
         "Topic: {topic}\nFocus keyword: {focus_keyword}\nTone: {tone}\n"
         "Word count target: {word_count}\nResearch points:\n{research}\n\n"
         "Create a detailed outline with H2 and H3 sections."),
    ])
    chain = prompt | llm | StrOutputParser()
    outline = await chain.ainvoke(state)
    return {**state, "outline": outline}


async def _draft_node(state: _ArticleGraphState) -> _ArticleGraphState:
    llm = _get_step_llm("draft")
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an expert content writer. Write a comprehensive, well-researched "
         "article in markdown format. Naturally incorporate the focus keyword. Use "
         "clear H2/H3 headings. Write short, scannable paragraphs. Include examples "
         "and data points."),
        ("human",
         "Topic: {topic}\nFocus keyword: {focus_keyword}\nTone: {tone}\n"
         "Language: {language}\nAudience: {target_audience}\nTarget: {word_count} words\n"
         "Research:\n{research}\nOutline:\n{outline}\n\n"
         "Write the complete article in markdown."),
    ])
    chain = prompt | llm | StrOutputParser()
    draft = await chain.ainvoke(state)
    return {**state, "draft": draft}


async def _edit_node(state: _ArticleGraphState) -> _ArticleGraphState:
    llm = _get_step_llm("review")
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a senior editor. Review and improve the article for clarity, "
         "flow, accuracy, and SEO. Fix any issues."),
        ("human",
         "Review and improve this article. Fix transitions, strengthen weak "
         "sections, ensure keyword integration:\n\n{draft}"),
    ])
    chain = prompt | llm | StrOutputParser()
    edited = await chain.ainvoke(state)
    return {**state, "edited_draft": edited}


async def _finalize_node(state: _ArticleGraphState) -> _ArticleGraphState:
    llm = _get_step_llm("seo")
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are an SEO specialist. Generate meta title (50-60 chars) and "
         "meta description (145-160 chars). Return only JSON."),
        ("human",
         "Topic: {topic}\nFocus keyword: {focus_keyword}\n"
         "Article preview:\n{preview}\n\n"
         'Return: {{"meta_title": "...", "meta_description": "..."}}'),
    ])
    chain = prompt | llm | StrOutputParser()
    seo_raw = await chain.ainvoke({**state, "preview": state["edited_draft"][:300]})

    meta_title, meta_description = "", ""
    try:
        m = re.search(r"\{.*\}", seo_raw, re.DOTALL)
        if m:
            data = json.loads(m.group())
            meta_title = data.get("meta_title", "")
            meta_description = data.get("meta_description", "")
    except Exception:
        pass

    return {
        **state,
        "final_article": state["edited_draft"],
        "meta_title": meta_title,
        "meta_description": meta_description,
    }


def _build_article_graph() -> StateGraph:
    graph = StateGraph(_ArticleGraphState)

    graph.add_node("research", _research_node)
    graph.add_node("outline", _outline_node)
    graph.add_node("draft", _draft_node)
    graph.add_node("edit", _edit_node)
    graph.add_node("finalize", _finalize_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "outline")
    graph.add_edge("outline", "draft")
    graph.add_edge("draft", "edit")
    graph.add_edge("edit", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()


_compiled_graph = None


def _get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = _build_article_graph()
    return _compiled_graph


class ArticleGraphService(IArticleAIService):
    """
    Implements IArticleAIService using a LangGraph 5-step pipeline.
    Each step uses a different LLM configured in ARTICLE_WRITER_LLM.
    """

    async def generate_article(
        self,
        *,
        topic: str,
        tone: str,
        language: str,
        target_audience: str,
        focus_keyword: str,
        word_count: int,
    ) -> ArticleAIResult:
        initial_state: _ArticleGraphState = {
            "topic": topic,
            "tone": tone,
            "language": language,
            "target_audience": target_audience,
            "focus_keyword": focus_keyword,
            "word_count": word_count,
            "research": "",
            "outline": "",
            "draft": "",
            "edited_draft": "",
            "final_article": "",
            "meta_title": "",
            "meta_description": "",
        }

        graph = _get_graph()
        final_state = await graph.ainvoke(initial_state)

        article_text = final_state.get("final_article", "")
        word_count_actual = len(article_text.split())
        tokens_estimated = word_count_actual * 4

        title_line = ""
        for line in article_text.split("\n"):
            stripped = line.strip().lstrip("#").strip()
            if stripped:
                title_line = stripped
                break

        return ArticleAIResult(
            title=title_line or topic,
            content=article_text,
            meta_title=final_state.get("meta_title", ""),
            meta_description=final_state.get("meta_description", ""),
            tokens_used=tokens_estimated,
        )
