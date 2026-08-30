from typing import List, Dict, Any

DEMO_SCENARIOS: List[Dict[str, Any]] = [
    {
        "id": "scenario-1",
        "scenario_code": "NORMAL_RETAIL",
        "title": "Normal Retail-Style Activity",
        "risk_level": "low",
        "expected_score": 12,
        "subject_type": "address",
        "subject_id": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
        "description": "Standard personal wallet transactions with low frequency, normal change outputs, and standard holding periods.",
        "judging_story": "Demonstrates a baseline retail user receiving routine transfers and sending occasional payments without rapid hops or splitting."
    },
    {
        "id": "scenario-2",
        "scenario_code": "RAPID_FORWARDING",
        "title": "Rapid Forwarding Pattern",
        "risk_level": "medium",
        "expected_score": 68,
        "subject_type": "address",
        "subject_id": "bc1qrapid83k92m1n0v9c8x7z6543210forward",
        "description": "Incoming Bitcoin is forwarded to a new destination within less than 3 minutes across multiple consecutive hops.",
        "judging_story": "Automated pass-through address forwarding full incoming amounts immediately to obscure funds origin."
    },
    {
        "id": "scenario-3",
        "scenario_code": "FAN_OUT_SPLITTING",
        "title": "Fan-Out Splitting Pattern",
        "risk_level": "high",
        "expected_score": 84,
        "subject_type": "address",
        "subject_id": "bc1qfanout9876543210split9876543210abc",
        "description": "A single input address disperses funds to 25+ distinct destination outputs in a single transaction batch.",
        "judging_story": "Dispersion technique used to split high-value funds into smaller unlinked outputs to evade static threshold monitoring."
    },
    {
        "id": "scenario-4",
        "scenario_code": "FAN_IN_CONSOLIDATION",
        "title": "Fan-In Consolidation Pattern",
        "risk_level": "medium",
        "expected_score": 62,
        "subject_type": "address",
        "subject_id": "bc1qfanin1234567890collect1234567890xyz",
        "description": "Multiple distinct source addresses sweep micro-balances into one central target wallet.",
        "judging_story": "Fund aggregation phase gathering dispersed balances prior to cashing out or moving to an exchange."
    },
    {
        "id": "scenario-5",
        "scenario_code": "PEELING_CHAIN",
        "title": "Peeling Chain Pattern",
        "risk_level": "high",
        "expected_score": 79,
        "subject_type": "transaction",
        "subject_id": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "description": "Sequential chain of transactions where a large value is systematically transferred forward while peeling off small change amounts.",
        "judging_story": "Classic peeling chain behavior common in unhosted wallet fund movement and mixing preprocesses."
    },
    {
        "id": "scenario-6",
        "scenario_code": "CIRCULAR_FLOW",
        "title": "Circular Flow Pattern",
        "risk_level": "high",
        "expected_score": 88,
        "subject_type": "address",
        "subject_id": "bc1qcycle000111222333444555666777888999",
        "description": "Funds move through 4 intermediate hop addresses and loop back to an entity closely connected to the origin.",
        "judging_story": "Artificial volume creation and wash-mixing pattern cycling value in closed entity loops."
    },
    {
        "id": "scenario-7",
        "scenario_code": "RISKY_NEIGHBOR",
        "title": "Known Risky-Neighbor Exposure",
        "risk_level": "critical",
        "expected_score": 94,
        "subject_type": "address",
        "subject_id": "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0",
        "description": "Direct 1-hop distance from a known flagged demo entity cluster (e.g. ransomware payload wallet).",
        "judging_story": "Direct exposure to high-priority flagged entities requiring immediate analyst triage and freezing recommendation."
    }
]

SEED_ALERTS = [
    {
        "id": "alt-001",
        "alert_code": "RISKY_NEIGHBOR_DIRECT",
        "title": "Direct Exposure to Flagged Demo Entity",
        "subject_type": "address",
        "subject_id": "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0",
        "risk_score": 94,
        "risk_level": "critical",
        "status": "new",
        "top_signal": "1-hop topological distance to flagged Ransomware cluster",
        "evidence": {
            "hops": 1,
            "flagged_entity": "DEMO_RANSOMWARE_PAYOUT_01",
            "exposure_amount_btc": 4.85
        },
        "created_at": "2026-08-27T08:30:00Z"
    },
    {
        "id": "alt-002",
        "alert_code": "CIRCULAR_LOOP_DETECTED",
        "title": "4-Hop Closed Cycle Detected",
        "subject_type": "address",
        "subject_id": "bc1qcycle000111222333444555666777888999",
        "risk_score": 88,
        "risk_level": "high",
        "status": "under_review",
        "top_signal": "Closed directed graph cycle spanning 4 intermediate entities",
        "evidence": {
            "cycle_length": 4,
            "volume_btc": 12.5
        },
        "created_at": "2026-08-27T07:15:00Z"
    },
    {
        "id": "alt-003",
        "alert_code": "FAN_OUT_SPLIT_HIGH",
        "title": "High-Volume Output Dispersal",
        "subject_type": "address",
        "subject_id": "bc1qfanout9876543210split9876543210abc",
        "risk_score": 84,
        "risk_level": "high",
        "status": "new",
        "top_signal": "Transaction dispersed funds across 28 distinct outputs",
        "evidence": {
            "outputs_count": 28,
            "total_dispersed_btc": 18.2
        },
        "created_at": "2026-08-27T06:45:00Z"
    },
    {
        "id": "alt-004",
        "alert_code": "PEELING_CHAIN_DETECTED",
        "title": "Sequential Peeling Flow",
        "subject_type": "transaction",
        "subject_id": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "risk_score": 79,
        "risk_level": "high",
        "status": "resolved",
        "top_signal": "Sequential 5-step peeling chain with minor change retention",
        "evidence": {
            "peel_steps": 5,
            "residual_change_avg_btc": 0.05
        },
        "created_at": "2026-08-26T22:10:00Z"
    },
    {
        "id": "alt-005",
        "alert_code": "RAPID_FORWARDING_BURST",
        "title": "Ultra-Short Forwarding Time Window",
        "subject_type": "address",
        "subject_id": "bc1qrapid83k92m1n0v9c8x7z6543210forward",
        "risk_score": 68,
        "risk_level": "medium",
        "status": "under_review",
        "top_signal": "Received funds forwarded in < 120 seconds",
        "evidence": {
            "time_delta_seconds": 114,
            "forwarded_ratio": 0.992
        },
        "created_at": "2026-08-26T18:00:00Z"
    }
]

ACTIVITY_TREND_DATA = [
    {"date": "2026-08-21", "low_count": 140, "medium_count": 22, "high_count": 8, "critical_count": 2},
    {"date": "2026-08-22", "low_count": 165, "medium_count": 19, "high_count": 11, "critical_count": 1},
    {"date": "2026-08-23", "low_count": 180, "medium_count": 28, "high_count": 14, "critical_count": 3},
    {"date": "2026-08-24", "low_count": 210, "medium_count": 31, "high_count": 9, "critical_count": 2},
    {"date": "2026-08-25", "low_count": 195, "medium_count": 24, "high_count": 15, "critical_count": 4},
    {"date": "2026-08-26", "low_count": 230, "medium_count": 35, "high_count": 18, "critical_count": 5},
    {"date": "2026-08-27", "low_count": 250, "medium_count": 42, "high_count": 21, "critical_count": 6},
]
