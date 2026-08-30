import os
from app.ml.feature_engineering import extract_feature_vector, FEATURE_NAMES
from app.ml.inference import MLInferenceEngine

def test_feature_vector_extraction():
    ctx = {
        "amount_btc": 15.5,
        "inputs_count": 2,
        "outputs_count": 10,
        "fee_btc": 0.002,
        "time_delta_seconds": 120,
        "peel_steps": 3,
        "dormant_days": 200,
        "micro_tx_count": 5,
        "hop_distance": 1,
        "tx_count_24h": 50,
        "volume_btc_24h": 75.0
    }
    vec = extract_feature_vector(ctx)
    assert len(vec) == len(FEATURE_NAMES)
    assert vec[0] == 15.5
    assert vec[8] == 1.0 # hop_distance

def test_ml_inference_with_model():
    engine = MLInferenceEngine()
    assert engine.ml_available is True

    result = engine.predict({
        "amount_btc": 20.0,
        "inputs_count": 1,
        "outputs_count": 15,
        "time_delta_seconds": 90,
        "peel_steps": 4,
        "dormant_days": 185,
        "hop_distance": 1,
        "tx_count_24h": 80,
        "volume_btc_24h": 120.0
    })

    assert result["ml_available"] is True
    assert 0.0 <= result["ml_score"] <= 35.0
    assert 0.0 <= result["graph_anomaly_score"] <= 25.0
    assert len(result["top_features"]) == 3

def test_ml_fallback_when_model_missing():
    # Pass non-existent path
    engine = MLInferenceEngine(model_path="non_existent_model.joblib")
    assert engine.ml_available is False

    result = engine.predict({"amount_btc": 1.0})
    assert result["ml_available"] is False
    assert result["message"] == "ML model unavailable; rule-based analysis used."
