"""Database models package."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    pass


from .user import LanguagePreference, User  # noqa: E402

__all__ = ["Base", "User", "LanguagePreference"]
