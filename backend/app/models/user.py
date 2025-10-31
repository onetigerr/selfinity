"""User model definition."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class LanguagePreference(enum.StrEnum):
    """Supported interface languages for a user profile."""

    RU = "ru"
    EN = "en"


class User(Base):
    """Application user."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    language_preference: Mapped[LanguagePreference] = mapped_column(
        Enum(
            LanguagePreference,
            name="language_preference_enum",
            values_callable=lambda x: [e.value for e in x],
        ),
        nullable=False,
        default=LanguagePreference.EN,
        server_default=LanguagePreference.EN.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
