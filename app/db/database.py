"""
TravelOS - Database Connection
Async SQLAlchemy engine and session management.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """
    Dependency: yields a database session.
    Automatically closes when the request ends.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
