import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.dataset.generator import SyntheticDatasetGenerator
from app.services.dataset.validator import DatasetValidator

client = TestClient(app)

def test_synthetic_dataset_generator_reproducibility():
    gen1 = SyntheticDatasetGenerator(seed=42)
    recs1 = gen1.generate_records(num_records=50)

    gen2 = SyntheticDatasetGenerator(seed=42)
    recs2 = gen2.generate_records(num_records=50)

    assert len(recs1) == 50
    assert len(recs2) == 50
    assert recs1[0]["transaction_id"] == recs2[0]["transaction_id"]
    assert recs1[0]["amount_btc"] == recs2[0]["amount_btc"]
    assert recs1[0]["scenario"] == recs2[0]["scenario"]

def test_dataset_validator_valid_content():
    gen = SyntheticDatasetGenerator(seed=123)
    recs = gen.generate_records(num_records=20)
    csv_str = gen.to_csv_string(recs)

    report = DatasetValidator.validate_csv_content(csv_str)
    assert report.is_valid is True
    assert report.total_rows_checked == 20
    assert report.error_count == 0

def test_dataset_validator_invalid_content():
    malformed_csv = (
        "transaction_id,timestamp,input_address,output_address,amount_btc\n"
        "tx001,invalid_date,not_an_address,not_an_address,-5.0\n"
        "tx001,2026-08-30T00:00:00Z,1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa,bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0,1.0\n"
    )

    report = DatasetValidator.validate_csv_content(malformed_csv)
    assert report.is_valid is False
    assert report.error_count > 0
    error_types = [e.error_type for e in report.errors]
    assert "DUPLICATE_TXID" in error_types or "INVALID_AMOUNT" in error_types

def test_dataset_api_generate_and_analyze_flow():
    # 1. Generate Dataset
    gen_payload = {
        "num_records": 30,
        "seed": 99,
        "scenario_distribution": {
            "normal": 0.5,
            "rapid_forwarding": 0.2,
            "peeling_chain": 0.3
        }
    }
    gen_res = client.post("/api/v1/dataset/generate", json=gen_payload)
    assert gen_res.status_code == 200
    gen_data = gen_res.json()
    assert "dataset_id" in gen_data
    dataset_id = gen_data["dataset_id"]
    assert gen_data["num_records"] == 30

    # 2. Download Dataset
    dl_res = client.get(f"/api/v1/dataset/download/{dataset_id}")
    assert dl_res.status_code == 200
    assert "text/csv" in dl_res.headers["content-type"]
    assert len(dl_res.content) > 0

    # 3. Analyze Generated Dataset
    ana_res = client.post(f"/api/v1/dataset/analyze/{dataset_id}")
    assert ana_res.status_code == 200
    ana_data = ana_res.json()
    assert ana_data["dataset_id"] == dataset_id
    assert ana_data["stats"]["total_transactions"] == 30
    assert len(ana_data["results"]) == 30
    assert ana_data["validation"]["is_valid"] is True
