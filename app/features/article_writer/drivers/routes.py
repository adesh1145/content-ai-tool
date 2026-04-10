"""
app/features/article_writer/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Long-Form Article Writer.
Uses LangGraph multi-step agent for deep research + writing.
POST /content/article
"""

from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import APIResponse
from app.features.article_writer.adapters.schemas import ArticleRequest, ArticleResponse
from app.features.article_writer.drivers.ai.article_graph import article_graph, ArticleState
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/article", tags=["Article Writer"])


@router.post("", response_model=APIResponse[ArticleResponse], status_code=201)
async def generate_article(
    body: ArticleRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate a long-form article using a LangGraph multi-step agent.

    Process (5 automated steps):
    1. **Research** — key angles, facts, expert perspectives
    2. **Outline** — detailed H2/H3 section structure
    3. **Draft** — complete article draft
    4. **Review** — editorial review and improvement
    5. **SEO** — meta title + description generation

    Note: This is a longer operation (15-45s). For production,
    consider using the async task endpoint with Celery.
    """
    try:
        initial_state: ArticleState = {
            "topic": body.topic,
            "tone": body.tone,
            "language": body.language,
            "target_audience": body.target_audience,
            "focus_keyword": body.focus_keyword or body.topic,
            "word_count": body.word_count,
            "research": "",
            "outline": "",
            "draft": "",
            "reviewed_draft": "",
            "final_article": "",
            "meta_title": "",
            "meta_description": "",
            "error": None,
        }

        final_state = await article_graph.ainvoke(initial_state)

        article_text = final_state.get("final_article", "")
        word_count = len(article_text.split())

        return APIResponse.ok(
            ArticleResponse(
                article_id=str(uuid.uuid4()),
                topic=body.topic,
                final_article=article_text,
                meta_title=final_state.get("meta_title", ""),
                meta_description=final_state.get("meta_description", ""),
                word_count=word_count,
                tokens_used=word_count * 4,  # Multi-step uses ~4x tokens
                status="completed",
            ),
            message="Long-form article generated successfully via 5-step AI agent.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Article generation failed: {e!s}")
