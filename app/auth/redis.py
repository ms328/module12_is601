# app/auth/redis.py
"""
Provide an async Redis interface used by the auth layer.

This module will try to use `redis.asyncio`. If that's not available
(for example in some CI environments where the package isn't installed),
it falls back to a lightweight in-memory async implementation that
implements the minimal subset used by the application (`from_url`,
`set`, `exists`). This keeps tests and CI stable without requiring an
actual Redis server or extra dependencies.
"""
from __future__ import annotations

import asyncio
import time
from typing import Optional

from app.core.config import get_settings

settings = get_settings()

# Try to import the official async redis client. If unavailable, provide
# a simple in-memory async fallback with the same minimal API used here.
try:
    import redis.asyncio as _redis_async  # type: ignore

    async def _create_redis(url: Optional[str]):
        return await _redis_async.from_url(url or "redis://localhost")

    _HAS_REAL_REDIS = True
except Exception:
    _HAS_REAL_REDIS = False

    class _InMemoryRedis:
        """A tiny async in-memory redis-like store used as a fallback.

        Only implements the minimal methods the app needs: `from_url` (async
        constructor), `set`, and `exists`. Expiry handling is supported via
        the `ex` parameter on `set`.
        """

        def __init__(self):
            self._data: dict[str, tuple[str, Optional[float]]] = {}
            self._lock = asyncio.Lock()

        @classmethod
        async def from_url(cls, url: Optional[str]):
            # kept async to match redis.asyncio.from_url behaviour
            return cls()

        async def set(self, key: str, value: str, ex: Optional[int] = None):
            expire = time.time() + ex if ex is not None else None
            async with self._lock:
                self._data[key] = (value, expire)

        async def exists(self, key: str) -> int:
            async with self._lock:
                item = self._data.get(key)
                if not item:
                    return 0
                _, expire = item
                if expire is not None and time.time() > expire:
                    # expired
                    del self._data[key]
                    return 0
                return 1

    async def _create_redis(url: Optional[str]):
        return await _InMemoryRedis.from_url(url)


async def get_redis():
    """Return a cached redis connection (real or in-memory fallback)."""
    if not hasattr(get_redis, "redis"):
        # Use the settings value if provided; keep call async to match both
        # real `_redis_async.from_url` and the fallback.
        get_redis.redis = await _create_redis(settings.REDIS_URL or "redis://localhost")
    return get_redis.redis


async def add_to_blacklist(jti: str, exp: int):
    """Add a token's JTI to the blacklist (with expiry in seconds)."""
    redis = await get_redis()
    await redis.set(f"blacklist:{jti}", "1", ex=exp)


async def is_blacklisted(jti: str) -> bool:
    """Return True if a token's JTI is blacklisted."""
    redis = await get_redis()
    exists = await redis.exists(f"blacklist:{jti}")
    # Some clients return int, others truthy values — normalize to bool
    return bool(exists)