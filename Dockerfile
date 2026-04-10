# =============================================================================
# Content AI Tool — Multi-Stage Dockerfile
# =============================================================================
# Stage 1: builder  → installs dependencies into a clean layer
# Stage 2: runner   → copies only what's needed (small final image)
# =============================================================================

# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

# System deps for compiling packages (cryptography, psycopg2, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy only requirements first (leverages Docker layer caching)
COPY requirements.txt .

# Install into a dedicated prefix so we can copy cleanly
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt && \
    pip install --prefix=/install --no-cache-dir email-validator


# ── Stage 2: Runner ───────────────────────────────────────────────────────────
FROM python:3.12-slim AS runner

LABEL maintainer="Content AI Tool"
LABEL description="AI Content Generation API — FastAPI + LangChain + LangGraph"

# Runtime system deps only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (security best practice)
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser

# Copy installed packages from builder
COPY --from=builder /install /usr/local

WORKDIR /app

# Copy application source
COPY --chown=appuser:appgroup app/ ./app/
COPY --chown=appuser:appgroup pyproject.toml .

# Create logs directory
RUN mkdir -p /app/logs && chown appuser:appgroup /app/logs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default: run FastAPI app
# Override CMD in docker-compose for celery worker
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
