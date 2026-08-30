from app.services.analysis.rule_engine import RuleEngine

rule_engine = RuleEngine()

def test_rule_rapid_forwarding():
    score, sig = rule_engine.evaluate_rapid_forwarding(120, 5.0)
    assert score > 0
    assert sig is not None
    assert sig.code == "RULE_RAPID_FORWARDING"
    assert "potentially suspicious" in sig.explanation.lower() or "potential" in sig.explanation.lower()

def test_rule_fan_out():
    score, sig = rule_engine.evaluate_fan_out(25, 10.0)
    assert score >= 10
    assert sig.code == "RULE_FAN_OUT_SPLITTING"

def test_rule_fan_in():
    score, sig = rule_engine.evaluate_fan_in(15, 8.0)
    assert score >= 8
    assert sig.code == "RULE_FAN_IN_CONSOLIDATION"

def test_rule_peeling_chain():
    score, sig = rule_engine.evaluate_peeling_chain(4, 0.02)
    assert score > 0
    assert sig.code == "RULE_PEELING_CHAIN"

def test_rule_dormancy_burst():
    score, sig = rule_engine.evaluate_dormancy_burst(200, 5)
    assert score > 0
    assert sig.code == "RULE_DORMANCY_BURST"

def test_rule_circular_flow():
    score, sig = rule_engine.evaluate_circular_flow(4, 15.0)
    assert score > 0
    assert sig.code == "RULE_CIRCULAR_FLOW"

def test_rule_structuring():
    score, sig = rule_engine.evaluate_structuring(8, 30.0)
    assert score > 0
    assert sig.code == "RULE_STRUCTURING"

def test_rule_risky_neighbor():
    score, sig = rule_engine.evaluate_risky_neighbor(1, "RANSOM_01")
    assert score == 20
    assert sig.severity == "critical"

def test_rule_amount_anomaly():
    score, sig = rule_engine.evaluate_amount_anomaly(50.0, 5.0, 2.0)
    assert score > 0
    assert sig.code == "RULE_AMOUNT_ANOMALY"

def test_rule_high_velocity():
    score, sig = rule_engine.evaluate_high_velocity(60, 100.0)
    assert score > 0
    assert sig.code == "RULE_HIGH_VELOCITY"

def test_rule_score_capping_at_40():
    # Context triggering multiple rules simultaneously
    context = {
        "time_delta_seconds": 60,
        "amount_btc": 10.0,
        "outputs_count": 30,
        "inputs_count": 25,
        "peel_steps": 5,
        "dormant_days": 300,
        "sudden_tx_count": 10,
        "cycle_length": 4,
        "micro_tx_count": 10,
        "window_minutes": 15,
        "hop_distance": 1,
        "flagged_cluster_name": "TEST_CLUSTER",
        "observed_value_btc": 100.0,
        "mean_btc": 10.0,
        "std_dev_btc": 5.0,
        "tx_count_24h": 100,
        "volume_btc_24h": 500.0
    }
    capped_score, signals = rule_engine.evaluate_all(context)
    assert capped_score <= 40
    assert len(signals) >= 5
