"""Tests for RedisCacheService."""

import pytest
from fakeredis.aioredis import FakeRedis

from app.shared.cache import RedisCacheService


@pytest.fixture
async def cache_service():
    """Fixture to provide a RedisCacheService using fakeredis."""
    service = RedisCacheService()
    # Inject fakeredis instead of real Redis
    service.redis = FakeRedis(decode_responses=True)
    yield service
    await service.close()


@pytest.mark.asyncio
async def test_cache_set_and_get(cache_service: RedisCacheService):
    """Test setting and getting a value from cache."""
    test_key = "test_key"
    test_value = {"hello": "world", "count": 1}

    # Set value
    await cache_service.set(test_key, test_value)

    # Get value
    cached_value = await cache_service.get(test_key)
    assert cached_value == test_value


@pytest.mark.asyncio
async def test_cache_delete(cache_service: RedisCacheService):
    """Test deleting a value from cache."""
    test_key = "test_key_delete"
    test_value = {"delete": "me"}

    await cache_service.set(test_key, test_value)

    # Ensure it's there
    assert await cache_service.get(test_key) is not None

    # Delete it
    await cache_service.delete(test_key)

    # Ensure it's gone
    assert await cache_service.get(test_key) is None


@pytest.mark.asyncio
async def test_cache_get_nonexistent(cache_service: RedisCacheService):
    """Test getting a nonexistent key returns None."""
    assert await cache_service.get("does_not_exist") is None
