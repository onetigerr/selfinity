import asyncio
import uuid
from typing import Generator

import pytest

from app.core.database import engine
from app.models import Base


@pytest.fixture(scope="session", autouse=True)
def create_db_schema() -> Generator[None, None, None]:
    async def _create():
        assert engine is not None
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Use asyncio.run to avoid deprecated get_event_loop warning on 3.12+
    asyncio.run(_create())
    yield


def test_register_success(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": email, "password": "secret12"}
    r = client.post("/auth/register", json=payload)

    assert r.status_code == 201
    data = r.json()
    assert data["email"] == payload["email"]
    assert data["language_preference"] == "en"
    assert "id" in data and "created_at" in data


def test_register_duplicate_email(client):
    email = f"dup_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": email, "password": "secret12"}
    r1 = client.post("/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Email already registered"


def test_login_success_and_get_me(client):
    email = f"login_{uuid.uuid4().hex[:8]}@example.com"
    password = "secret12"
    client.post("/auth/register", json={"email": email, "password": password})

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    user = me.json()
    assert user["email"] == email


def test_login_wrong_password(client):
    email = f"wrong_{uuid.uuid4().hex[:8]}@example.com"
    client.post("/auth/register", json={"email": email, "password": "secret12"})

    r = client.post("/auth/login", json={"email": email, "password": "badpass"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid credentials"


def test_get_me_unauthorized(client):
    r = client.get("/auth/me")
    assert r.status_code == 401
    assert r.json()["detail"] in {"Missing Authorization header", "Invalid Authorization header"}
