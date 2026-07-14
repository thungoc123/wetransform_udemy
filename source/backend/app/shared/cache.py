"""
Cache Service Module.

This module provides a Singleton RedisCacheService for interacting with Redis.
"""

import json
from typing import Any

import structlog
from redis.asyncio import Redis, from_url  # type: ignore

from app.config import settings

logger = structlog.get_logger("cache")


class RedisCacheService:
    """Service to interact with Redis for caching."""

    def __init__(self) -> None:
        self.redis: Redis | None = None

    async def init_cache(self) -> None:
        """Initialize the Redis connection pool."""
        try:
            self.redis = from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_timeout=5,
            )
            # Test connection
            await self.redis.ping()
            logger.info("redis_connected", url=settings.REDIS_URL)
        except Exception as e:
            logger.error("redis_connection_failed", error=str(e))
            self.redis = None

    async def close(self) -> None:
        """Close the Redis connection pool."""
        if self.redis:
            await self.redis.aclose()
            logger.info("redis_closed")

    async def get(self, key: str) -> dict[str, Any] | None:
        """Get a value from cache."""
        if not self.redis:
            return None
        try:
            data = await self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.warning("redis_get_failed", key=key, error=str(e))
            return None

    async def set(
        self, key: str, value: dict[str, Any], ttl_seconds: int = 3600
    ) -> None:
        """Set a value in cache with expiration."""
        if not self.redis:
            return
        try:
            await self.redis.set(key, json.dumps(value), ex=ttl_seconds)
        except Exception as e:
            logger.warning("redis_set_failed", key=key, error=str(e))

    async def delete(self, key: str) -> None:
        """Delete a key from cache."""
        if not self.redis:
            return
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.warning("redis_delete_failed", key=key, error=str(e))


# Global Singleton instance
redis_cache = RedisCacheService()
