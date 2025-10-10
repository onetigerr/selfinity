"""Async database engine and session utilities."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from .config import get_settings

engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None


def init_engine(database_url: Optional[str] = None, *, echo: bool = False) -> None:
    """Initialise SQLAlchemy async engine and session factory."""
    global engine, AsyncSessionLocal  # Module-level singletons configured once at startup.
    url = database_url or get_settings().database_url
    engine = create_async_engine(url, echo=echo)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the configured async session factory."""
    if AsyncSessionLocal is None:
        init_engine()
    assert AsyncSessionLocal is not None  # for type checkers
    return AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for request-scoped usage."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session


# Initialise engine when module loads so application is ready by default.
init_engine()
