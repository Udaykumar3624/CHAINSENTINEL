from fastapi.testclient import TestClient
from app.main import app
from app.seed.seed_data import DEMO_SCENARIOS, SEED_ALERTS

client = TestClient(app)

def test_seeded_scenario_counts():
    response = client.get("/api/v1/demo/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == len(DEMO_SCENARIOS)
    assert len(data["scenarios"]) == 7

def test_seeded_alerts_count():
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(SEED_ALERTS)

def test_seeded_dashboard_kpis():
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    kpis = data["kpis"]
    assert kpis["total_transactions_analyzed"] >= 0
    assert kpis["high_critical_alerts"] >= 0
    assert kpis["open_cases"] >= 0
    assert kpis["flagged_clusters"] >= 0
