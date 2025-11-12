from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base  # <-- Use absolute import
import os
from contextlib import asynccontextmanager

# Load the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db/template_db")

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (good for dev)
    future=True
)

# Create a configured "AsyncSession" class
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    """
    Dependency to get an async database session.
    Ensures the session is always closed.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

async def create_db_and_tables():
    """
    Initializes the database and creates tables on startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db_connection():
    """
    Closes the database connection pool on shutdown.
    """
    await engine.dispose()