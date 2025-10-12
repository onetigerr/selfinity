"""Async repository for User entities."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LanguagePreference, User


class UserRepository:
    """Data access for users using an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, *, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        self.session.add(user)
        await self.session.flush()  # obtain PK
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_language(self, user_id: uuid.UUID, language: str) -> User:
        # Validate language via enum; raises ValueError on invalid
        lang = LanguagePreference(language)
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(language_preference=lang)
            .returning(User)
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one()
        await self.session.commit()
        return user

