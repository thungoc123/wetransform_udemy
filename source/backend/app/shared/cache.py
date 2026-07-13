import json
from typing import Any, Optional
import redis.asyncio as redis
from app.config import settings
import structlog

logger = structlog.get_logger(__name__)

# Initialize Redis client
redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

async def get_cache(key: str) -> Optional[Any]:
    try:
        val = await redis_client.get(key)
        return json.loads(val) if val else None
    except Exception as e:
        logger.error("redis_get_failed", key=key, error=str(e))
        return None

async def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    try:
        await redis_client.set(key, json.dumps(value), ex=expire)
        return True
    except Exception as e:
        logger.error("redis_set_failed", key=key, error=str(e))
        return False
