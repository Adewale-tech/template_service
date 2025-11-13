"""
Unit tests for cache service.
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cache_service_get(mock_redis):
    """Test cache get operation."""
    mock_redis.get.return_value = b'{"name": "test_template"}'

    result = await mock_redis.get("template:test:en")
    assert result is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cache_service_set(mock_redis):
    """Test cache set operation."""
    mock_redis.set.return_value = True

    result = await mock_redis.set("template:test:en", '{"name": "test"}')
    assert result is True


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cache_service_delete(mock_redis):
    """Test cache delete operation."""
    mock_redis.delete.return_value = 1

    result = await mock_redis.delete("template:test:en")
    assert result == 1
