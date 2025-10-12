import sys
from collections.abc import AsyncGenerator

import python_multipart.multipart as python_multipart_multipart
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

sys.modules.setdefault("multipart", python_multipart_multipart)
from fastapi.testclient import TestClient

from app.core.config import get_settings  # noqa: E402
from app.core.database import get_session_factory, init_engine  # noqa: E402
from app.main import create_application  # noqa: E402

get_settings.cache_clear()
init_engine()


@pytest.fixture(scope="session")
def app_instance():
    """Provide a FastAPI application instance for tests."""
    return create_application()


@pytest.fixture()
def client(app_instance):
    """Synchronous test client for FastAPI app."""
    with TestClient(app_instance) as test_client:
        yield test_client


@pytest.fixture()
async def async_client(app_instance) -> AsyncGenerator[AsyncClient, None]:
    """HTTPX async client for testing async endpoints."""
    transport = ASGITransport(app=app_instance)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
    await transport.aclose()


@pytest.fixture()
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session bound to the in-memory SQLite database."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session
