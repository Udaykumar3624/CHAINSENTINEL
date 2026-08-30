from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_alerts_list():
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    assert data[0]["alert_code"] is not None

def test_get_alerts_filter_critical():
    response = client.get("/api/v1/alerts?risk_level=critical")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(a["risk_level"] == "critical" for a in data)

def test_get_alert_by_id_found():
    response = client.get("/api/v1/alerts/alt-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "alt-001"
    assert data["risk_level"] == "critical"

def test_get_alert_by_id_not_found():
    response = client.get("/api/v1/alerts/nonexistent-id")
    assert response.status_code == 404
