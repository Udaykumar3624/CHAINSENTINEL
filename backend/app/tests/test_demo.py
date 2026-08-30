from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_demo_scenarios_endpoint():
    response = client.get("/api/v1/demo/scenarios")
    assert response.status_code == 200
    data = response.json()
    
    assert "scenarios" in data
    assert data["count"] == 7
    assert len(data["scenarios"]) == 7
    assert data["mode"] == "deterministic_offline"
    
    codes = [s["scenario_code"] for s in data["scenarios"]]
    assert "NORMAL_RETAIL" in codes
    assert "RISKY_NEIGHBOR" in codes
