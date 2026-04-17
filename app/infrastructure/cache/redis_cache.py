from __future__ import annotations

import json
from typing import Any

import logging

from app.common.port.outbound.cache_port import CachePort

logger = logging.getLogger(__name__)


class RedisCacheAdapter(CachePort):
    """Redis implementation of the cache port."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0") -> None:
        try:
            import redis.asyncio as aioredis
            self._redis = aioredis.from_url(redis_url, decode_responses=True)
        except ImportError:
            logger.warning("redis package not available, cache operations will fail")
            self._redis = None

    async def get(self, key: str) -> Any | None:
        if not self._redis:
            return None
        value = await self._redis.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    async def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        if not self._redis:
            return
        serialized = json.dumps(value) if not isinstance(value, str) else value
        await self._redis.set(key, serialized, ex=ttl_seconds)

    async def delete(self, key: str) -> bool:
        if not self._redis:
            return False
        return bool(await self._redis.delete(key))

    async def exists(self, key: str) -> bool:
        if not self._redis:
            return False
        return bool(await self._redis.exists(key))
