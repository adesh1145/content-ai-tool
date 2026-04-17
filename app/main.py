"""
app/main.py
─────────────────────────────────────────────────────────────
FastAPI application factory.

Registers all feature routers, global exception handlers,
middleware (CORS, logging), and startup events.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    DomainException,
    NotFoundError,
    QuotaExceededError,
    ValidationError,
)
from app.core.response import APIResponse
from app.core.utils.logger import logger, setup_logging
from app.infrastructure.db.connection import create_all_tables

settings = get_settings()


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup / shutdown events."""
    setup_logging(debug=settings.DEBUG)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION} [{settings.APP_ENV}]")
    logger.info(f"📦 LLM Provider: {settings.LLM_PROVIDER.upper()} ({settings.OPENAI_MODEL if settings.LLM_PROVIDER == 'openai' else settings.ANTHROPIC_MODEL})")

    # Create DB tables (dev only — use alembic in production)
    await create_all_tables()
    logger.info("✅ Database tables ready")

    yield

    logger.info("👋 Shutting down...")


# ── App Factory ───────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Industry-grade AI Content Generation API\n\n"
            "## Features\n"
            "- 🖊️ **Blog Generator** — SEO-optimised blog posts with meta tags\n"
            "- 📰 **Article Writer** — Long-form articles via 5-step LangGraph agent\n"
            "- 📱 **Social Media** — LinkedIn, Twitter/X, Instagram posts\n"
            "- 📣 **Ad Copy** — Google Ads (AIDA) + Facebook Ads (PAS) with A/B variations\n"
            "- 🛍️ **Product Descriptions** — F-A-B framework ecommerce copy\n"
            "- ✉️ **Email Writer** — Cold email, newsletter, follow-up, welcome\n"
            "- 🎬 **Script Writer** — YouTube, Reels, Podcast scripts\n"
            "- 🔍 **SEO Optimizer** — Content analysis, scoring, meta generation\n"
            "- 🔐 **Auth** — JWT authentication + API key management\n"
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── Middlewares ───────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()
        
        logger.info(f"Incoming request {request.method} {request.url.path} [ID: {request_id}]")
        
        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            logger.info(
                f"Completed request {request.method} {request.url.path} "
                f"[ID: {request_id}] - Status: {response.status_code} - Time: {process_time:.4f}s"
            )
            return response
        except Exception as e:
            process_time = time.perf_counter() - start_time
            logger.error(
                f"Failed request {request.method} {request.url.path} "
                f"[ID: {request_id}] - Error: {str(e)} - Time: {process_time:.4f}s"
            )
            raise

    # ── Exception Handlers ────────────────────────────────────────────────────
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content=APIResponse.error(exc.message, exc.code).model_dump(),
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content=APIResponse.error(exc.message, exc.code).model_dump(),
        )

    @app.exception_handler(AuthenticationError)
    async def auth_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(
            status_code=401,
            content=APIResponse.error(exc.message, exc.code).model_dump(),
        )

    @app.exception_handler(AuthorizationError)
    async def authz_handler(request: Request, exc: AuthorizationError):
        return JSONResponse(
            status_code=403,
            content=APIResponse.error(exc.message, exc.code).model_dump(),
        )

    @app.exception_handler(QuotaExceededError)
    async def quota_handler(request: Request, exc: QuotaExceededError):
        return JSONResponse(
            status_code=429,
            content=APIResponse.error(exc.message, exc.code).model_dump(),
        )

    @app.exception_handler(DomainException)
    async def domain_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=400,
            content=APIResponse.error(exc.message, exc.code).model_dump(),
        )

    # ── Register Feature Routers ──────────────────────────────────────────────
    prefix = settings.API_PREFIX

    from app.features.auth.drivers.routes import router as auth_router
    from app.features.blog_generator.drivers.routes import router as blog_router
    from app.features.article_writer.drivers.routes import router as article_router
    from app.features.social_media.drivers.routes import router as social_router
    from app.features.ad_copy.drivers.routes import router as ad_router
    from app.features.product_description.drivers.routes import router as product_router
    from app.features.email_writer.drivers.routes import router as email_router
    from app.features.script_writer.drivers.routes import router as script_router
    from app.features.seo_optimizer.drivers.routes import router as seo_router

    app.include_router(auth_router, prefix=prefix)
    app.include_router(blog_router, prefix=prefix)
    app.include_router(article_router, prefix=prefix)
    app.include_router(social_router, prefix=prefix)
    app.include_router(ad_router, prefix=prefix)
    app.include_router(product_router, prefix=prefix)
    app.include_router(email_router, prefix=prefix)
    app.include_router(script_router, prefix=prefix)
    app.include_router(seo_router, prefix=prefix)

    # ── Health Check ──────────────────────────────────────────────────────────
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
