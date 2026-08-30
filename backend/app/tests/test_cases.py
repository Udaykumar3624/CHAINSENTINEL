from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_cases_list():
    response = client.get("/api/v1/cases")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_create_case():
    payload = {
        "title": "Suspected Wash Trading Cluster Analysis",
        "description": "Investigating high frequency circular fund transfers across 4 addresses.",
        "priority": "high",
        "status": "open",
        "assigned_investigator": "Demo Investigator",
        "linked_addresses": ["bc1qcycle000111222333444555666777888999"]
    }
    response = client.post("/api/v1/cases", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["case_number"].startswith("CASE-2026-")
    assert data["title"] == payload["title"]
    assert len(data["linked_addresses"]) == 1

def test_add_case_note():
    # Fetch first case
    cases_resp = client.get("/api/v1/cases")
    case_id = cases_resp.json()[0]["id"]

    note_payload = {
        "note_text": "Completed preliminary graph trace. Node 1-hop distance confirmed to ransom cluster.",
        "author_name": "Demo Investigator"
    }
    response = client.post(f"/api/v1/cases/{case_id}/notes", json=note_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["case_id"] == case_id
    assert data["note_text"] == note_payload["note_text"]

def test_update_alert_status():
    response = client.patch("/api/v1/alerts/alt-001", json={"status": "under_review"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "alt-001"
    assert data["status"] == "under_review"

def test_update_alert_invalid_status():
    response = client.patch("/api/v1/alerts/alt-001", json={"status": "invalid_status"})
    assert response.status_code == 400
