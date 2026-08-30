from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ChainSentinel"
    assert "disclaimer" in data
    assert "guilt" not in data["disclaimer"].lower() or "not constitute legal proof" in data["disclaimer"].lower()

def test_api_v1_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["environment"] is not None
