"""_summary_ ."""

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


# def test_root():
#     """_summary_ ."""
#     response = client.get("/")
#     assert response.status_code == 200


def test_health():
    """_summary_ ."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"msg": "API is healthy"}
