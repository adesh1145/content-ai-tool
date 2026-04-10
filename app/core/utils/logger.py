"""
app/core/utils/logger.py
────────────────────────────────────────────────────────────
Structured logging setup using Loguru.

Import `logger` from here everywhere in the project.
"""

from __future__ import annotations

import sys

from loguru import logger


def setup_logging(debug: bool = False) -> None:
    """Configure Loguru for structured, levelled logging."""
    logger.remove()  # Remove default handler

    level = "DEBUG" if debug else "INFO"
    fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    logger.add(sys.stdout, format=fmt, level=level, colorize=True)
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format=fmt,
    )


__all__ = ["logger", "setup_logging"]
