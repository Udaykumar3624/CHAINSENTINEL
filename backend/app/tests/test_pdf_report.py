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
