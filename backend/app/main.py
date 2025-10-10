from fastapi import FastAPI

from .api.health import router as health_router
from .core.config import get_settings


def create_application() -> FastAPI:
    """Create and configure a FastAPI application instance."""
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    app.include_router(health_router, prefix="/health", tags=["health"])
    return app


app = create_application()

