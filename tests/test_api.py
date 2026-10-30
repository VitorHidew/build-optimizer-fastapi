from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok", "dataset": "ficticio"}


def test_invalid_target_returns_400():
    response = client.get("/api/optimize", params={"target_id": "inexistente"})
    assert response.status_code == 400
