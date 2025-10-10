from datetime import datetime


def test_health_endpoint_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database"] == "connected"
    assert payload["timestamp"] == "2025-10-10T15:06:00Z"

    # Validate timestamp format (ISO 8601 with UTC designator).
    datetime.strptime(payload["timestamp"], "%Y-%m-%dT%H:%M:%SZ")


async def test_health_endpoint_async(async_client):
    response = await async_client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload == {
        "status": "ok",
        "timestamp": "2025-10-10T15:06:00Z",
        "database": "connected",
    }

