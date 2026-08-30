import numpy as np
from typing import Dict, Any, List

FEATURE_NAMES: List[str] = [
    "amount_btc",
    "inputs_count",
    "outputs_count",
    "fee_btc",
    "time_delta_seconds",
    "peel_steps",
    "dormant_days",
    "micro_tx_count",
    "hop_distance",
    "tx_count_24h",
    "volume_btc_24h"
]

def extract_feature_vector(context: Dict[str, Any]) -> List[float]:
    """Convert transaction or address context dictionary into normalized numeric feature vector."""
    return [
        float(context.get("amount_btc", 1.0)),
        float(context.get("inputs_count", 1)),
        float(context.get("outputs_count", 2)),
        float(context.get("fee_btc", 0.0005)),
        float(context.get("time_delta_seconds", 3600)),
        float(context.get("peel_steps", 0)),
        float(context.get("dormant_days", 0)),
        float(context.get("micro_tx_count", 0)),
        float(context.get("hop_distance", 5)), # 5 = default far distance
        float(context.get("tx_count_24h", 5)),
        float(context.get("volume_btc_24h", 2.0))
    ]

def get_feature_names() -> List[str]:
    return FEATURE_NAMES
