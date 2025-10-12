import uuid
from httpx import ASGITransport, AsyncClient

from app.main import create_application


async def test_full_registration_flow():
    app = create_application()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        email = f"int_{uuid.uuid4().hex[:8]}@example.com"
        password = "secret12"

        r1 = await client.post("/auth/register", json={"email": email, "password": password})
        assert r1.status_code == 201
        user = r1.json()
        assert user["email"] == email

        r2 = await client.post("/auth/login", json={"email": email, "password": password})
        assert r2.status_code == 200
        token = r2.json()["access_token"]
        assert token

        r3 = await client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r3.status_code == 200
        me = r3.json()
        assert me["email"] == email

