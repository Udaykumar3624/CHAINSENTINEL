from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_export_pdf_report_endpoint():
    cases_resp = client.get("/api/v1/cases")
    case_id = cases_resp.json()[0]["id"]

    response = client.get(f"/api/v1/cases/{case_id}/report.pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000
    # PDF magic header check (%PDF-)
    assert response.content.startswith(b"%PDF-")

def test_export_investigation_pdf_endpoints():
    payload = {
        "subject_id": "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0",
        "risk_score": 84,
        "risk_level": "high",
        "composite_risk_score": 84,
        "signals": [
            {"code": "RULE_RISKY_NEIGHBOR", "severity": "critical", "score_contribution": 20, "title": "1-Hop Exposure to Flagged Ransomware Cluster"}
        ],
        "network_context": {
            "source_ip": "13.225.103.55",
            "source_country": "India",
            "source_asn": "AS16509",
            "source_asn_org": "Amazon.com, Inc.",
            "destination_ip": "185.220.101.5",
            "destination_country": "Germany",
            "destination_asn": "AS60729",
            "destination_asn_org": "Stiftung Erneuerbare Freiheit"
        }
    }

    # 1. Analyze route
    resp1 = client.post("/api/v1/analyze/export-pdf", json=payload)
    assert resp1.status_code == 200
    assert resp1.headers["content-type"] == "application/pdf"
    assert resp1.content.startswith(b"%PDF-")

    # 2. Cases route
    resp2 = client.post("/api/v1/cases/export-investigation-pdf", json=payload)
    assert resp2.status_code == 200
    assert resp2.headers["content-type"] == "application/pdf"
    assert resp2.content.startswith(b"%PDF-")

