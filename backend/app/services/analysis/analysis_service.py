from datetime import datetime, timezone
from typing import Dict, Any, List
from app.services.analysis.rule_engine import RuleEngine
from app.ml.inference import MLInferenceEngine
from app.schemas.analysis import AnalysisResultResponse, RiskDecomposition, SignalItem
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

"""
===============================================================================
CHAINSENTINEL COMPOSITE RISK SCORE NORMALIZATION & AGGREGATION FORMULA
===============================================================================

Composite Risk Score (C) is a 0–100 bounded prioritization score derived from
three independent analysis sub-engines:

1. Rule Engine (R): Range [0.0, 40.0]
   - Sum of contributions from 10 deterministic behavioral heuristic rules.
   - Formula: R = min(40.0, sum(rule_score_i for i in 1..10))

2. ML Baseline Engine (M): Range [0.0, 35.0]
   - Supervised risk probability output from RandomForestClassifier (P_risk in [0, 1]).
   - Formula: M = round(P_risk * 35.0, 1)
   - Fallback (if model missing): M_fallback = round((R / 40.0) * 35.0, 1)

3. Graph & Anomaly Engine (G): Range [0.0, 25.0]
   - Unsupervised IsolationForest anomaly score (A_score in [0, 1]) + graph topology bonus.
   - Formula: G = min(25.0, round(A_score * 15.0 + graph_centrality_bonus, 1))
   - Fallback (if model missing): G_fallback = round((R / 40.0) * 25.0, 1)

Composite Score Aggregation:
   C = min(100, round(R + M + G))

Risk Level & Category Mapping:
   - C >= 75: CRITICAL (Immediate freezing protocol & multi-hop investigation required)
   - 50 <= C < 75: HIGH (Prioritize human analyst triage)
   - 25 <= C < 50: MEDIUM (Flag for standard periodic monitoring)
   - C < 25: LOW (Standard transaction flow; low risk)

Disclaimer:
   Risk scores are behavioral prioritization signals for human analysts, NOT legal proof of crime.
===============================================================================
"""

class AnalysisService:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.ml_engine = MLInferenceEngine()

    def analyze_address(self, address: str, context: Dict[str, Any] = None) -> AnalysisResultResponse:
        return self.analyze_subject("address", address, context)

    def analyze_transaction(self, txid: str, context: Dict[str, Any] = None) -> AnalysisResultResponse:
        return self.analyze_subject("transaction", txid, context)

    def analyze_subject(self, subject_type: str, subject_id: str, context: Dict[str, Any] = None) -> AnalysisResultResponse:
        ctx = context or self._build_demo_context(subject_id)

        # 1. Rule Engine Evaluation (0-40)
        rule_score, signals = self.rule_engine.evaluate_all(ctx)

        # 2. ML Baseline & Anomaly Inference (0-35 ML, 0-25 Graph/Anomaly)
        ml_result = self.ml_engine.predict(ctx)
        is_ml_fallback = not ml_result["ml_available"]

        if not is_ml_fallback:
            ml_score = ml_result["ml_score"]
            graph_score = ml_result["graph_anomaly_score"]
        else:
            # Fallback mode: heuristic allocation based on rule intensity
            ml_score = round((rule_score / 40.0) * 35.0, 1)
            graph_score = round((rule_score / 40.0) * 25.0, 1)

        # Composite score capping at 100
        composite_score = min(100, int(round(rule_score + ml_score + graph_score)))

        # Risk Level & Category Mapping
        if composite_score >= 75:
            risk_level = "critical"
            risk_category = "CRITICAL"
            recommended_action = "CRITICAL RISK EXPOSURE: Immediate freezing protocol & multi-hop graph expansion required."
        elif composite_score >= 50:
            risk_level = "high"
            risk_category = "HIGH"
            recommended_action = "HIGH BEHAVIORAL RISK: Prioritize human analyst triage and trace funding origin."
        elif composite_score >= 25:
            risk_level = "medium"
            risk_category = "MEDIUM"
            recommended_action = "MODERATE ANOMALY: Flag for standard periodic monitoring."
        else:
            risk_level = "low"
            risk_category = "LOW"
            recommended_action = "LOW RISK PATTERN: Standard transaction flow; no action required."

        # Extract triggered indicator codes
        triggered_indicators = [sig.code for sig in signals]

        # Disclaimer
        disclaimer = RESPONSIBLE_AI_DISCLAIMER
        if is_ml_fallback:
            disclaimer += " | NOTE: ML model unavailable; rule-based analysis used."

        return AnalysisResultResponse(
            subject_type=subject_type,
            subject_id=subject_id,
            risk_score=composite_score,
            risk_level=risk_level,
            composite_risk_score=composite_score,
            risk_category=risk_category,
            rule_score=round(rule_score, 1),
            ml_score=round(ml_score, 1),
            graph_score=round(graph_score, 1),
            confidence=0.88 if not is_ml_fallback else 0.75,
            score_decomposition=RiskDecomposition(
                rule_score=round(rule_score, 1),
                ml_score=round(ml_score, 1),
                graph_score=round(graph_score, 1)
            ),
            triggered_indicators=triggered_indicators,
            feature_values=ctx,
            evidence=signals,
            signals=signals,
            recommended_action=recommended_action,
            data_source="ChainSentinel Risk Engine",
            is_ml_fallback=is_ml_fallback,
            disclaimer=disclaimer,
            analyzed_at=datetime.now(timezone.utc).isoformat()
        )

    def _build_demo_context(self, subject_id: str) -> Dict[str, Any]:
        if "9x08" in subject_id or "ransom" in subject_id:
            return {
                "amount_btc": 24.5,
                "inputs_count": 1,
                "outputs_count": 12,
                "fee_btc": 0.005,
                "time_delta_seconds": 180,
                "peel_steps": 4,
                "dormant_days": 210,
                "micro_tx_count": 8,
                "hop_distance": 1,
                "tx_count_24h": 65,
                "volume_btc_24h": 85.0,
                "known_flagged_neighbor": True
            }
        elif "cycle" in subject_id:
            return {
                "amount_btc": 10.0,
                "inputs_count": 2,
                "outputs_count": 2,
                "fee_btc": 0.001,
                "time_delta_seconds": 300,
                "has_cycle": True,
                "cycle_length": 4,
                "hop_distance": 2,
                "tx_count_24h": 25,
                "volume_btc_24h": 40.0
            }
        else:
            return {
                "amount_btc": 0.5,
                "inputs_count": 1,
                "outputs_count": 2,
                "fee_btc": 0.0001,
                "time_delta_seconds": 3600,
                "dormant_days": 5,
                "hop_distance": 5,
                "tx_count_24h": 2,
                "volume_btc_24h": 1.0
            }
