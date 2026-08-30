import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_address_endpoint():
    response = client.post("/api/v1/analyze/address", json={"address": "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0"})
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["risk_score"] <= 100
    assert data["risk_level"] in ["low", "medium", "high", "critical"]
    assert "score_decomposition" in data
    assert data["score_decomposition"]["rule_score"] <= 40
    assert "disclaimer" in data
    # Responsible AI check
    assert "guilt" not in data["recommended_action"].lower() or "not constitute legal proof" in data["disclaimer"].lower()

def test_analyze_transaction_endpoint():
    response = client.post("/api/v1/analyze/transaction", json={"txid": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"})
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["risk_score"] <= 100
    assert data["subject_type"] == "transaction"

def test_risk_score_bounds_guarantee():
    # Test extreme inputs to ensure score never leaves 0-100 range
    response = client.post("/api/v1/analyze/address", json={"address": "bc1qcycle000111222333444555666777888999"})
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["risk_score"] <= 100
    assert 0 <= data["score_decomposition"]["rule_score"] <= 40
    assert 0 <= data["score_decomposition"]["ml_score"] <= 35
    assert 0 <= data["score_decomposition"]["graph_score"] <= 25

def test_analyze_csv_valid_file():
    csv_content = (
        "tx_hash,source_address,destination_address,amount_btc,timestamp\n"
        "tx001,1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa,bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0,2.5,2026-08-27T00:00:00Z\n"
        "tx002,bc1qrapid83k92m1n0v9c8x7z6543210forward,bc1qfanout9876543210split9876543210abc,15.0,2026-08-27T01:00:00Z\n"
    )
    files = {"file": ("test_batch.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/v1/analyze/csv", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["total_rows_processed"] == 2
    assert len(data["results"]) == 2

def test_analyze_csv_invalid_extension():
    files = {"file": ("test_data.txt", io.BytesIO(b"dummy text"), "text/plain")}
    response = client.post("/api/v1/analyze/csv", files=files)
    assert response.status_code == 400
    assert "Only .csv files are supported" in response.json()["detail"]

def test_analyze_csv_missing_columns():
    csv_content = "tx_hash,amount_btc\ntx001,2.5\n"
    files = {"file": ("bad_header.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    response = client.post("/api/v1/analyze/csv", files=files)
    assert response.status_code == 400
    assert "Missing required CSV columns" in response.json()["detail"]
