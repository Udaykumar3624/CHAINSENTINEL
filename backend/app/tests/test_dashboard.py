from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_summary_endpoint():
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    
    assert "kpis" in data
    assert data["kpis"]["total_transactions_analyzed"] >= 0
    assert data["kpis"]["high_critical_alerts"] >= 0
    
    assert "risk_distribution" in data
    assert "critical" in data["risk_distribution"]
    
    assert "recent_alerts" in data
    assert len(data["recent_alerts"]) >= 0
    assert "disclaimer" in data
