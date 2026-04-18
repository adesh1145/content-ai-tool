"""
app/infrastructure/celery/worker.py
─────────────────────────────────────────────────────────────
Celery async task worker configuration.

Used for long-running content generation tasks (article_writer, blog).
Redis is used as both the broker and result backend.
"""

from __future__ import annotations

from celery import Celery

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "content_ai_tool",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=3600,  # Results kept for 1 hour
)
