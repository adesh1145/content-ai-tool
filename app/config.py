"""Backward-compatible shim — re-exports from app.common.config.settings."""

from app.common.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
