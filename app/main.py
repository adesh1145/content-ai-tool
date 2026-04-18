"""
app/main.py
Application factory — FastAPI entry point.
Clean Architecture + Hexagonal + DDD + SOLID.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.common.config.openapi_config import OPENAPI_DESCRIPTION
from app.common.config.settings import get_settings
from app.common.exception.global_exception_handler import register_exception_handlers
from app.common.middleware.cors_middleware import register_cors
from app.common.middleware.request_logging_middleware import RequestLoggingMiddleware
from app.infrastructure.db.connection import create_all_tables

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )
    logger.info("Starting %s v%s [%s]", settings.APP_NAME, settings.APP_VERSION, settings.APP_ENV)
    logger.info("LLM Provider: %s", settings.LLM_PROVIDER.upper())

    await create_all_tables()
    logger.info("Database tables ready")

    yield

    logger.info("Shutting down...")


def _register_feature_routers(app: FastAPI) -> None:
    prefix = settings.API_PREFIX

    from app.features.auth.presentation.rest.controller import router as auth_router
    from app.features.blog_generator.presentation.rest.controller import router as blog_router
    from app.features.article_writer.presentation.rest.controller import router as article_router
    from app.features.social_media.presentation.rest.controller import router as social_router
    from app.features.ad_copy.presentation.rest.controller import router as ad_router
    from app.features.product_description.presentation.rest.controller import router as product_router
    from app.features.email_writer.presentation.rest.controller import router as email_router
    from app.features.script_writer.presentation.rest.controller import router as script_router
    from app.features.seo_optimizer.presentation.rest.controller import router as seo_router

    app.include_router(auth_router, prefix=prefix)
    app.include_router(blog_router, prefix=prefix)
    app.include_router(article_router, prefix=prefix)
    app.include_router(social_router, prefix=prefix)
    app.include_router(ad_router, prefix=prefix)
    app.include_router(product_router, prefix=prefix)
    app.include_router(email_router, prefix=prefix)
    app.include_router(script_router, prefix=prefix)
    app.include_router(seo_router, prefix=prefix)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=OPENAPI_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    register_cors(app)
    app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(app)
    _register_feature_routers(app)

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "env": settings.APP_ENV,
            "llm_provider": settings.LLM_PROVIDER,
        }

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": f"Welcome to {settings.APP_NAME} API",
            "docs": "/docs",
            "version": settings.APP_VERSION,
        }

    return app


app = create_app()
