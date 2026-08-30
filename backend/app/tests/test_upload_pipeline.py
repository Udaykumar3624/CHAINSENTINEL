import io
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.dataset.parser import UniversalDatasetParser

client = TestClient(app)

SAMPLE_CSV_CONTENT = """transaction_id,timestamp,input_address,output_address,amount_btc,scenario,label
tx_csv_001,2026-08-30T12:00:00Z,bc1qcsv01,bc1qcsv02,2.5,rapid_forwarding,suspicious
tx_csv_002,2026-08-30T12:05:00Z,bc1qcsv02,bc1qcsv03,2.4,normal,normal
"""

SAMPLE_JSON_CONTENT = """[
  {
    "txid": "tx_json_001",
    "datetime": "2026-08-30T14:00:00Z",
    "from_address": "bc1qjson01",
    "to_address": "bc1qjson02",
    "amount": 1.75,
    "pattern": "peeling_chain",
    "target": "suspicious"
  }
]"""

SAMPLE_TXT_CONTENT = """tx_txt_001,2026-08-30T16:00:00Z,bc1qtxt01,bc1qtxt02,0.9,circular_flow,suspicious
tx_txt_002,2026-08-30T16:05:00Z,bc1qtxt02,bc1qtxt03,0.85,normal,normal
"""

def test_universal_parser_csv():
    res = UniversalDatasetParser.parse_content(SAMPLE_CSV_CONTENT, "test.csv")
    assert res.is_valid
    assert res.total_records_parsed == 2
    assert res.normalized_transactions[0].transaction_id == "tx_csv_001"
    assert res.normalized_transactions[0].amount_btc == 2.5

def test_universal_parser_json():
    res = UniversalDatasetParser.parse_content(SAMPLE_JSON_CONTENT, "test.json")
    assert res.is_valid
    assert res.total_records_parsed == 1
    assert res.normalized_transactions[0].transaction_id == "tx_json_001"
    assert res.normalized_transactions[0].input_address == "bc1qjson01"

def test_universal_parser_txt():
    res = UniversalDatasetParser.parse_content(SAMPLE_TXT_CONTENT, "test.txt")
    assert res.is_valid
    assert res.total_records_parsed == 2
    assert res.normalized_transactions[0].transaction_id == "tx_txt_001"

def test_upload_csv_endpoint():
    files = {"file": ("my_test.csv", io.BytesIO(SAMPLE_CSV_CONTENT.encode("utf-8")), "text/csv")}
    res = client.post("/api/v1/dataset/upload", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["summary"]["total_transactions"] == 2
    assert data["data_source_type"] == "Uploaded Dataset"

def test_upload_json_endpoint():
    files = {"file": ("my_test.json", io.BytesIO(SAMPLE_JSON_CONTENT.encode("utf-8")), "application/json")}
    res = client.post("/api/v1/dataset/upload", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["summary"]["total_transactions"] == 1

def test_upload_txt_endpoint():
    files = {"file": ("my_test.txt", io.BytesIO(SAMPLE_TXT_CONTENT.encode("utf-8")), "text/plain")}
    res = client.post("/api/v1/dataset/upload", files=files)
    assert res.status_code == 200
    data = res.json()
    assert data["summary"]["total_transactions"] == 2

def test_upload_invalid_file_extension():
    files = {"file": ("malicious.exe", io.BytesIO(b"binary"), "application/octet-stream")}
    res = client.post("/api/v1/dataset/upload", files=files)
    assert res.status_code == 400

def test_dashboard_reflects_uploaded_dataset():
    # 1. Reset Dashboard
    client.post("/api/v1/dashboard/reset")
    res_empty = client.get("/api/v1/dashboard/summary")
    assert res_empty.json()["kpis"]["total_transactions_analyzed"] == 0

    # 2. Upload CSV dataset with 2 transactions
    files = {"file": ("dynamic_test.csv", io.BytesIO(SAMPLE_CSV_CONTENT.encode("utf-8")), "text/csv")}
    client.post("/api/v1/dataset/upload", files=files)

    # 3. Dashboard must now equal 2
    res_dash = client.get("/api/v1/dashboard/summary")
    dash_data = res_dash.json()
    assert dash_data["kpis"]["total_transactions_analyzed"] == 2
    assert dash_data["active_dataset"]["data_source_type"] == "Uploaded Dataset"
