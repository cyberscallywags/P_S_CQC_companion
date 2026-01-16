"""_summary_ ."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health():
    """_summary_ ."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "msg": "API is healthy",
        "database": "unhealthy",
    }
