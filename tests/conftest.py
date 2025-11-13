"""
Pytest configuration and shared fixtures.
"""
import pytest
import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
def mock_redis():
    """Create mock Redis client."""
    return AsyncMock()


@pytest.fixture
def mock_rabbitmq_channel():
    """Create mock RabbitMQ channel."""
    return AsyncMock()


@pytest.fixture
def mock_settings():
    """Create mock settings."""
    return {
        "APP_NAME": "Template Service",
        "DEBUG": True,
        "ENVIRONMENT": "testing"
    }
