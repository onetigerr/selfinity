"""Authentication service with registration, login and current user logic."""

from __future__ import annotations

import uuid
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError

from app.core import security
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse


class AuthService:
    """Encapsulates auth flows using repository and security helpers."""

    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    async def register(self, payload: UserRegisterRequest) -> UserResponse:
        existing = await self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        pwd_hash = security.hash_password(payload.password)
        user = await self.repo.create(email=payload.email, password_hash=pwd_hash)
        return UserResponse.model_validate(user)

    async def login(self, payload: UserLoginRequest) -> TokenResponse:
        user = await self.repo.get_by_email(payload.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not security.verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = security.create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=token)

    async def get_current_user(self, token: str) -> UserResponse:
        try:
            payload = security.decode_access_token(token)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        try:
            user_id = uuid.UUID(str(sub))
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return UserResponse.model_validate(user)

