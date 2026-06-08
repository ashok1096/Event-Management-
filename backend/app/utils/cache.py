"""Redis cache-aside helper for EventPulse.

Usage:
    from app.utils.cache import get_cache, set_cache, delete_cache, invalidate_prefix

    # Store a value (auto JSON-serialised)
    await set_cache("event:1", event_dict, ttl=300)

    # Retrieve a value (returns None on miss)
    data = await get_cache("event:1")

    # Delete a specific key
    await delete_cache("event:1")

    # Invalidate all keys with a prefix (e.g. after bulk update)
    await invalidate_prefix("event:")
"""

import os
import json
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Optional Redis dependency – app still works if Redis is unavailable.
# ---------------------------------------------------------------------------
try:
    import redis.asyncio as aioredis  # pip install redis[asyncio]
    _REDIS_AVAILABLE = True
except ImportError:
    _REDIS_AVAILABLE = False

_redis_client: Optional[Any] = None

DEFAULT_TTL = int(os.getenv("CACHE_TTL_SECONDS", "300"))  # 5 minutes


async def init_cache() -> None:
    """Initialise the Redis connection pool.  Call once from main.py lifespan."""
    global _redis_client

    if not _REDIS_AVAILABLE:
        logger.warning("redis package not installed – cache disabled.")
        return

    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    try:
        _redis_client = aioredis.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
            socket_connect_timeout=2,
        )
        await _redis_client.ping()
        logger.info("Redis cache connected", extra={"redis_url": redis_url})
    except Exception as exc:
        logger.warning("Redis unavailable – cache disabled.", extra={"error": str(exc)})
        _redis_client = None


async def close_cache() -> None:
    """Close the Redis connection pool.  Call from main.py lifespan teardown."""
    global _redis_client
    if _redis_client:
        await _redis_client.aclose()
        _redis_client = None


async def get_cache(key: str) -> Optional[Any]:
    """Return the cached value for *key*, or None on a miss / error."""
    if _redis_client is None:
        return None
    try:
        raw = await _redis_client.get(key)
        return json.loads(raw) if raw is not None else None
    except Exception as exc:
        logger.warning("Cache GET failed", extra={"key": key, "error": str(exc)})
        return None


async def set_cache(key: str, value: Any, ttl: int = DEFAULT_TTL) -> None:
    """Serialise *value* to JSON and store it under *key* with a TTL."""
    if _redis_client is None:
        return
    try:
        await _redis_client.setex(key, ttl, json.dumps(value, default=str))
    except Exception as exc:
        logger.warning("Cache SET failed", extra={"key": key, "error": str(exc)})


async def delete_cache(key: str) -> None:
    """Delete a single cache entry."""
    if _redis_client is None:
        return
    try:
        await _redis_client.delete(key)
    except Exception as exc:
        logger.warning("Cache DELETE failed", extra={"key": key, "error": str(exc)})


async def invalidate_prefix(prefix: str) -> None:
    """Delete all keys that start with *prefix* (e.g. 'event:')."""
    if _redis_client is None:
        return
    try:
        keys = await _redis_client.keys(f"{prefix}*")
        if keys:
            await _redis_client.delete(*keys)
            logger.info("Cache invalidated", extra={"prefix": prefix, "count": len(keys)})
    except Exception as exc:
        logger.warning("Cache invalidate_prefix failed", extra={"prefix": prefix, "error": str(exc)})
