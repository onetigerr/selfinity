from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db

router = APIRouter()


@router.get("", summary="Health check")
async def health_check(
    session: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Verify application and database availability."""
    await session.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "timestamp": "2025-10-10T15:06:00Z",
        "database": "connected",
    }
