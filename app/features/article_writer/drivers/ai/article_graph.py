"""
app/features/article_writer/drivers/ai/article_graph.py
─────────────────────────────────────────────────────────────
LangGraph multi-step article writing agent.

Graph nodes:
  1. research_node   → Identify angles, sources, key points
  2. outline_node    → Create detailed section structure  
  3. draft_node      → Write each section
  4. review_node     → Self-review and improve
  5. seo_node        → Add SEO optimisation
"""

from __future__ import annotations
from typing import TypedDict
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from app.infrastructure.ai.llm_factory import get_llm_provider


class ArticleState(TypedDict):
    topic: str
    tone: str
    language: str
    target_audience: str
    focus_keyword: str
    word_count: int
    research: str
    outline: str
    draft: str
    reviewed_draft: str
    final_article: str
    meta_title: str
    meta_description: str
    error: str | None


def _get_llm():
    provider = get_llm_provider()
    from app.infrastructure.ai.llm_factory import OpenAIProvider, AnthropicProvider
    if isinstance(provider, (OpenAIProvider, AnthropicProvider)):
        return provider.get_langchain_llm()
    raise RuntimeError("Unsupported provider")


async def research_node(state: ArticleState) -> ArticleState:
    """Node 1: Research the topic — key angles, facts, expert opinions."""
    llm = _get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research assistant. Identify the most important angles, facts, statistics, and expert perspectives for the given topic."),
        ("human", "Topic: {topic}\nAudience: {target_audience}\nKeyword: {focus_keyword}\n\nList 5-7 key research points, facts, and angles. Be specific."),
    ])
    chain = prompt | llm | StrOutputParser()
    research = await chain.ainvoke(state)
    return {**state, "research": research}


async def outline_node(state: ArticleState) -> ArticleState:
    """Node 2: Create detailed article outline with sections."""
    llm = _get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a content strategist. Create a detailed article outline optimised for SEO and reader engagement."),
        ("human", (
            "Topic: {topic}\nFocus keyword: {focus_keyword}\nTone: {tone}\n"
            "Word count target: {word_count}\nResearch points:\n{research}\n\n"
            "Create a detailed outline with H2 and H3 sections."
        )),
    ])
    chain = prompt | llm | StrOutputParser()
    outline = await chain.ainvoke(state)
    return {**state, "outline": outline}


async def draft_node(state: ArticleState) -> ArticleState:
    """Node 3: Write the full article draft."""
    llm = _get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert content writer. Write a comprehensive, well-researched article "
            "in markdown format. Naturally incorporate the focus keyword. Use clear H2/H3 headings. "
            "Write short, scannable paragraphs. Include examples and data points."
        )),
        ("human", (
            "Topic: {topic}\nFocus keyword: {focus_keyword}\nTone: {tone}\n"
            "Language: {language}\nAudience: {target_audience}\nTarget: {word_count} words\n"
            "Research:\n{research}\nOutline:\n{outline}\n\nWrite the complete article in markdown."
        )),
    ])
    chain = prompt | llm | StrOutputParser()
    draft = await chain.ainvoke(state)
    return {**state, "draft": draft}


async def review_node(state: ArticleState) -> ArticleState:
    """Node 4: Self-review and improve the draft."""
    llm = _get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior editor. Review and improve the article for clarity, flow, accuracy, and SEO. Fix any issues."),
        ("human", "Review and improve this article. Fix transitions, strengthen weak sections, ensure keyword integration:\n\n{draft}"),
    ])
    chain = prompt | llm | StrOutputParser()
    reviewed = await chain.ainvoke(state)
    return {**state, "reviewed_draft": reviewed}


async def seo_node(state: ArticleState) -> ArticleState:
    """Node 5: Generate SEO metadata for the final article."""
    import json, re
    llm = _get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an SEO specialist. Generate meta title (50-60 chars) and meta description (145-160 chars). Return only JSON."),
        ("human", "Topic: {topic}\nFocus keyword: {focus_keyword}\nArticle preview:\n{preview}\n\nReturn: {{\"meta_title\": \"...\", \"meta_description\": \"...\"}}"),
    ])
    chain = prompt | llm | StrOutputParser()
    seo_raw = await chain.ainvoke({**state, "preview": state["reviewed_draft"][:300]})

    meta_title, meta_description = "", ""
    try:
        m = re.search(r"\{.*\}", seo_raw, re.DOTALL)
        if m:
            data = json.loads(m.group())
            meta_title = data.get("meta_title", "")
            meta_description = data.get("meta_description", "")
    except Exception:
        pass

    return {**state, "final_article": state["reviewed_draft"], "meta_title": meta_title, "meta_description": meta_description}


def build_article_graph() -> StateGraph:
    """Build and compile the LangGraph article writing graph."""
    graph = StateGraph(ArticleState)

    graph.add_node("research", research_node)
    graph.add_node("outline", outline_node)
    graph.add_node("draft", draft_node)
    graph.add_node("review", review_node)
    graph.add_node("seo", seo_node)

    graph.set_entry_point("research")
    graph.add_edge("research", "outline")
    graph.add_edge("outline", "draft")
    graph.add_edge("draft", "review")
    graph.add_edge("review", "seo")
    graph.add_edge("seo", END)

    return graph.compile()


# Compiled graph singleton
article_graph = build_article_graph()
