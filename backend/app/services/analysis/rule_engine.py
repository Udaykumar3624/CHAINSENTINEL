import math
from typing import List, Dict, Any, Tuple
from app.schemas.analysis import SignalItem

# Rule Engine Configuration Thresholds
CONFIG_THRESHOLDS = {
    "rapid_forwarding_seconds": 600,       # 10 minutes
    "fan_out_outputs_min": 10,              # > 10 outputs
    "fan_in_inputs_min": 10,                # > 10 inputs
    "peeling_chain_min_steps": 3,           # >= 3 sequential peeling hops
    "dormancy_days_min": 180,               # 6 months inactivity
    "structuring_max_amount_btc": 0.1,      # <= 0.1 BTC per micro tx
    "structuring_min_count": 5,             # >= 5 micro txs
    "high_velocity_volume_btc": 50.0,       # > 50 BTC in 24h
    "high_velocity_tx_count": 50,           # > 50 txs in 24h
    "amount_anomaly_std_dev": 3.0,          # > 3 std devs
}

class RuleEngine:
    def __init__(self, thresholds: Dict[str, Any] = None):
        self.thresholds = thresholds or CONFIG_THRESHOLDS

    def evaluate_rapid_forwarding(self, time_delta_seconds: float, amount_btc: float) -> Tuple[int, SignalItem | None]:
        if time_delta_seconds < self.thresholds["rapid_forwarding_seconds"]:
            score = 12 if time_delta_seconds < 180 else 8
            signal = SignalItem(
                code="RULE_RAPID_FORWARDING",
                title="Rapid Forwarding Pattern",
                severity="high" if score >= 10 else "medium",
                score_contribution=score,
                explanation=f"Received funds were forwarded within {int(time_delta_seconds)} seconds (< {self.thresholds['rapid_forwarding_seconds']}s threshold). This represents potential automated pass-through risk exposure requiring human review.",
                observed_values={"time_delta_seconds": time_delta_seconds, "amount_btc": amount_btc},
                recommended_review_step="Inspect destination wallets to verify if funds are being routed to an unhosted wallet or mixing service."
            )
            return score, signal
        return 0, None

    def evaluate_fan_out(self, outputs_count: int, total_amount_btc: float) -> Tuple[int, SignalItem | None]:
        if outputs_count >= self.thresholds["fan_out_outputs_min"]:
            score = 15 if outputs_count >= 25 else 10
            signal = SignalItem(
                code="RULE_FAN_OUT_SPLITTING",
                title="Fan-Out Dispersal Pattern",
                severity="high",
                score_contribution=score,
                explanation=f"Transaction dispersed funds across {outputs_count} distinct output destinations (>= {self.thresholds['fan_out_outputs_min']} threshold). High fan-out represents potential splitting behavior.",
                observed_values={"outputs_count": outputs_count, "total_amount_btc": total_amount_btc},
                recommended_review_step="Cross-reference destination addresses against exchange deposit patterns."
            )
            return score, signal
        return 0, None

    def evaluate_fan_in(self, inputs_count: int, total_amount_btc: float) -> Tuple[int, SignalItem | None]:
        if inputs_count >= self.thresholds["fan_in_inputs_min"]:
            score = 12 if inputs_count >= 20 else 8
            signal = SignalItem(
                code="RULE_FAN_IN_CONSOLIDATION",
                title="Fan-In Consolidation Pattern",
                severity="medium",
                score_contribution=score,
                explanation=f"Transaction collected inputs from {inputs_count} separate source addresses (>= {self.thresholds['fan_in_inputs_min']} threshold). Represents potential balance consolidation.",
                observed_values={"inputs_count": inputs_count, "total_amount_btc": total_amount_btc},
                recommended_review_step="Review source wallet cluster history for prior coordinated activity."
            )
            return score, signal
        return 0, None

    def evaluate_peeling_chain(self, peel_steps: int, avg_change_btc: float) -> Tuple[int, SignalItem | None]:
        if peel_steps >= self.thresholds["peeling_chain_min_steps"]:
            score = 14
            signal = SignalItem(
                code="RULE_PEELING_CHAIN",
                title="Peeling Chain Pattern",
                severity="high",
                score_contribution=score,
                explanation=f"Sequential transfers exhibit {peel_steps} consecutive peeling steps peeling off small change ({avg_change_btc:.4f} BTC avg). Represents potential unhosted wallet peeling behavior.",
                observed_values={"peel_steps": peel_steps, "avg_change_btc": avg_change_btc},
                recommended_review_step="Trace the remaining main output branch to identify final consolidation point."
            )
            return score, signal
        return 0, None

    def evaluate_dormancy_burst(self, dormant_days: float, sudden_tx_count: int) -> Tuple[int, SignalItem | None]:
        if dormant_days >= self.thresholds["dormancy_days_min"] and sudden_tx_count >= 3:
            score = 10
            signal = SignalItem(
                code="RULE_DORMANCY_BURST",
                title="Dormancy Burst Pattern",
                severity="medium",
                score_contribution=score,
                explanation=f"Address was inactive for {int(dormant_days)} days before sudden activity burst ({sudden_tx_count} transactions). Represents potential dormant account reactivation indicator.",
                observed_values={"dormant_days": dormant_days, "sudden_tx_count": sudden_tx_count},
                recommended_review_step="Check historical creation period of address for older security incidents."
            )
            return score, signal
        return 0, None

    def evaluate_circular_flow(self, cycle_length: int, circular_volume_btc: float) -> Tuple[int, SignalItem | None]:
        if cycle_length >= 3:
            score = 15
            signal = SignalItem(
                code="RULE_CIRCULAR_FLOW",
                title="Circular Flow Pattern",
                severity="high",
                score_contribution=score,
                explanation=f"Graph analysis identified a closed transaction cycle involving {cycle_length} entities ({circular_volume_btc:.2f} BTC volume). Represents potential wash transfer risk indicator.",
                observed_values={"cycle_length": cycle_length, "circular_volume_btc": circular_volume_btc},
                recommended_review_step="Analyze entity ownership connections across all nodes in the detected cycle."
            )
            return score, signal
        return 0, None

    def evaluate_structuring(self, micro_tx_count: int, window_minutes: float) -> Tuple[int, SignalItem | None]:
        if micro_tx_count >= self.thresholds["structuring_min_count"]:
            score = 12
            signal = SignalItem(
                code="RULE_STRUCTURING",
                title="Structuring (Smurfing) Indicator",
                severity="high",
                score_contribution=score,
                explanation=f"Observed {micro_tx_count} small transfers below 0.1 BTC within {int(window_minutes)} minutes. Represents potential structuring indicator requiring human review.",
                observed_values={"micro_tx_count": micro_tx_count, "window_minutes": window_minutes},
                recommended_review_step="Aggregate total combined volume across all small transfers to evaluate true threshold exposure."
            )
            return score, signal
        return 0, None

    def evaluate_risky_neighbor(self, hop_distance: int, flagged_cluster_name: str) -> Tuple[int, SignalItem | None]:
        if hop_distance <= 2:
            score = 20 if hop_distance == 1 else 10
            signal = SignalItem(
                code="RULE_RISKY_NEIGHBOR",
                title="Known Flagged Entity Exposure",
                severity="critical" if hop_distance == 1 else "high",
                score_contribution=score,
                explanation=f"Direct {hop_distance}-hop topological distance to known demo flagged entity '{flagged_cluster_name}'. Represents potential high risk exposure requiring immediate review.",
                observed_values={"hop_distance": hop_distance, "flagged_cluster_name": flagged_cluster_name},
                recommended_review_step="Review complete transaction history between subject and flagged entity."
            )
            return score, signal
        return 0, None

    def evaluate_amount_anomaly(self, observed_value_btc: float, mean_btc: float, std_dev_btc: float) -> Tuple[int, SignalItem | None]:
        if std_dev_btc > 0:
            z_score = abs(observed_value_btc - mean_btc) / std_dev_btc
            if z_score >= self.thresholds["amount_anomaly_std_dev"]:
                score = 8
                signal = SignalItem(
                    code="RULE_AMOUNT_ANOMALY",
                    title="Transaction Amount Anomaly",
                    severity="medium",
                    score_contribution=score,
                    explanation=f"Observed transaction amount ({observed_value_btc:.2f} BTC) is {z_score:.1f} standard deviations away from subject baseline. Represents potential behavioral anomaly indicator.",
                    observed_values={"observed_value_btc": observed_value_btc, "mean_btc": mean_btc, "z_score": round(z_score, 2)},
                    recommended_review_step="Compare transaction timing with historical trading pattern changes."
                )
                return score, signal
        return 0, None

    def evaluate_high_velocity(self, tx_count_24h: int, volume_btc_24h: float) -> Tuple[int, SignalItem | None]:
        if volume_btc_24h >= self.thresholds["high_velocity_volume_btc"] or tx_count_24h >= self.thresholds["high_velocity_tx_count"]:
            score = 10
            signal = SignalItem(
                code="RULE_HIGH_VELOCITY",
                title="High Velocity Activity",
                severity="medium",
                score_contribution=score,
                explanation=f"High 24-hour activity observed ({tx_count_24h} txs, {volume_btc_24h:.2f} BTC volume). Exceeds high-velocity triage threshold.",
                observed_values={"tx_count_24h": tx_count_24h, "volume_btc_24h": volume_btc_24h},
                recommended_review_step="Evaluate if entity is an exchange hot wallet or high-frequency automated service."
            )
            return score, signal
        return 0, None

    def evaluate_all(self, context: Dict[str, Any]) -> Tuple[int, List[SignalItem]]:
        total_raw_score = 0
        signals: List[SignalItem] = []

        # 1. Rapid forwarding
        if "time_delta_seconds" in context and "amount_btc" in context:
            score, sig = self.evaluate_rapid_forwarding(context["time_delta_seconds"], context["amount_btc"])
            total_raw_score += score
            if sig: signals.append(sig)

        # 2. Fan-out
        if "outputs_count" in context:
            score, sig = self.evaluate_fan_out(context["outputs_count"], context.get("total_amount_btc", 0.0))
            total_raw_score += score
            if sig: signals.append(sig)

        # 3. Fan-in
        if "inputs_count" in context:
            score, sig = self.evaluate_fan_in(context["inputs_count"], context.get("total_amount_btc", 0.0))
            total_raw_score += score
            if sig: signals.append(sig)

        # 4. Peeling chain
        if "peel_steps" in context:
            score, sig = self.evaluate_peeling_chain(context["peel_steps"], context.get("avg_change_btc", 0.0))
            total_raw_score += score
            if sig: signals.append(sig)

        # 5. Dormancy burst
        if "dormant_days" in context and "sudden_tx_count" in context:
            score, sig = self.evaluate_dormancy_burst(context["dormant_days"], context["sudden_tx_count"])
            total_raw_score += score
            if sig: signals.append(sig)

        # 6. Circular flow
        if "cycle_length" in context:
            score, sig = self.evaluate_circular_flow(context["cycle_length"], context.get("circular_volume_btc", 0.0))
            total_raw_score += score
            if sig: signals.append(sig)

        # 7. Structuring
        if "micro_tx_count" in context and "window_minutes" in context:
            score, sig = self.evaluate_structuring(context["micro_tx_count"], context["window_minutes"])
            total_raw_score += score
            if sig: signals.append(sig)

        # 8. Risky neighbor
        if "hop_distance" in context and "flagged_cluster_name" in context:
            score, sig = self.evaluate_risky_neighbor(context["hop_distance"], context["flagged_cluster_name"])
            total_raw_score += score
            if sig: signals.append(sig)

        # 9. Amount anomaly
        if "observed_value_btc" in context and "mean_btc" in context and "std_dev_btc" in context:
            score, sig = self.evaluate_amount_anomaly(context["observed_value_btc"], context["mean_btc"], context["std_dev_btc"])
            total_raw_score += score
            if sig: signals.append(sig)

        # 10. High velocity
        if "tx_count_24h" in context and "volume_btc_24h" in context:
            score, sig = self.evaluate_high_velocity(context["tx_count_24h"], context["volume_btc_24h"])
            total_raw_score += score
            if sig: signals.append(sig)

        # Cap Rule Score strictly between 0 and 40
        capped_rule_score = min(40, max(0, total_raw_score))
        return capped_rule_score, signals
