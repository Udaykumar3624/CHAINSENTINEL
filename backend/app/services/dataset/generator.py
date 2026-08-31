import io
import os
import csv
import random
from hashlib import sha256
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Tuple

# Fix typo sha256 import
def generate_txid(seed_str: str) -> str:
    return sha256(seed_str.encode('utf-8')).hexdigest()

def generate_btc_address(prefix: str, index: int) -> str:
    hash_part = sha256(f"{prefix}_{index}".encode('utf-8')).hexdigest()[:34].lower()
    if prefix.startswith("legacy"):
        return f"1{hash_part[:33]}"
    elif prefix.startswith("p2sh"):
        return f"3{hash_part[:33]}"
    else:
        return f"bc1q{hash_part[:38]}"

SCENARIOS = [
    "normal",
    "rapid_forwarding",
    "fan_out",
    "fan_in",
    "peeling_chain",
    "circular_flow",
    "dormancy_burst",
    "structuring",
    "risky_neighbor"
]

class SyntheticDatasetGenerator:
    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = random.Random(seed)

    def generate_records(self, num_records: int = 100, distribution: Dict[str, float] = None) -> List[Dict[str, Any]]:
        self.rng.seed(self.seed)
        
        # Default scenario probabilities if not provided
        if not distribution:
            distribution = {
                "normal": 0.40,
                "rapid_forwarding": 0.10,
                "fan_out": 0.10,
                "fan_in": 0.10,
                "peeling_chain": 0.08,
                "circular_flow": 0.06,
                "dormancy_burst": 0.06,
                "structuring": 0.05,
                "risky_neighbor": 0.05
            }

        # Normalize weights
        scenarios_list = list(distribution.keys())
        weights = [distribution[s] for s in scenarios_list]
        total_w = sum(weights)
        norm_weights = [w / total_w for w in weights]

        base_time = datetime(2026, 8, 1, 0, 0, 0, tzinfo=timezone.utc)
        base_block = 850000

        records: List[Dict[str, Any]] = []

        for i in range(1, num_records + 1):
            chosen_scenario = self.rng.choices(scenarios_list, weights=norm_weights, k=1)[0]
            label = "normal" if chosen_scenario == "normal" else "suspicious"

            txid = generate_txid(f"synth_tx_{self.seed}_{i}_{chosen_scenario}")
            block_height = base_block + (i // 6)

            if chosen_scenario == "normal":
                time_delta = self.rng.randint(1800, 43200) # 30 mins to 12 hours
                amount_btc = round(self.rng.uniform(0.01, 2.5), 4)
                input_count = self.rng.choice([1, 2])
                output_count = self.rng.choice([1, 2])
                input_addr = generate_btc_address("norm_in", i)
                output_addr = generate_btc_address("norm_out", i)
                unique_counterparties = input_count + output_count
                tx_size = self.rng.randint(220, 250)
                fee_btc = round(amount_btc * 0.0001 + 0.00005, 6)

            elif chosen_scenario == "rapid_forwarding":
                time_delta = self.rng.randint(30, 180) # 30s to 3m
                amount_btc = round(self.rng.uniform(5.0, 45.0), 4)
                input_count = 1
                output_count = 2
                input_addr = generate_btc_address("rapid_in", i)
                output_addr = generate_btc_address("rapid_out", i)
                unique_counterparties = 3
                tx_size = 225
                fee_btc = 0.0015

            elif chosen_scenario == "fan_out":
                time_delta = self.rng.randint(300, 3600)
                amount_btc = round(self.rng.uniform(15.0, 80.0), 4)
                input_count = 1
                output_count = self.rng.randint(12, 35)
                input_addr = generate_btc_address("fanout_in", i)
                output_addr = generate_btc_address("fanout_out", i)
                unique_counterparties = 1 + output_count
                tx_size = 150 + (output_count * 34)
                fee_btc = 0.0035

            elif chosen_scenario == "fan_in":
                time_delta = self.rng.randint(300, 3600)
                amount_btc = round(self.rng.uniform(20.0, 90.0), 4)
                input_count = self.rng.randint(15, 40)
                output_count = 1
                input_addr = generate_btc_address("fanin_in", i)
                output_addr = generate_btc_address("fanin_out", i)
                unique_counterparties = input_count + 1
                tx_size = 200 + (input_count * 148)
                fee_btc = 0.0042

            elif chosen_scenario == "peeling_chain":
                time_delta = self.rng.randint(120, 600)
                amount_btc = round(self.rng.uniform(10.0, 50.0), 4)
                input_count = 1
                output_count = 2 # 1 main payload, 1 peel change
                input_addr = generate_btc_address("peel_in", i)
                output_addr = generate_btc_address("peel_out", i)
                unique_counterparties = 3
                tx_size = 224
                fee_btc = 0.0008

            elif chosen_scenario == "circular_flow":
                time_delta = self.rng.randint(200, 900)
                amount_btc = round(self.rng.uniform(8.0, 30.0), 4)
                input_count = 2
                output_count = 2
                input_addr = f"bc1qcycle_{self.seed}_node_{i % 3}"
                output_addr = f"bc1qcycle_{self.seed}_node_{(i + 1) % 3}"
                unique_counterparties = 3
                tx_size = 250
                fee_btc = 0.0012

            elif chosen_scenario == "dormancy_burst":
                time_delta = self.rng.randint(600, 3600)
                amount_btc = round(self.rng.uniform(30.0, 120.0), 4)
                input_count = 1
                output_count = 3
                input_addr = generate_btc_address("dormant_in", i)
                output_addr = generate_btc_address("dormant_out", i)
                unique_counterparties = 4
                tx_size = 280
                fee_btc = 0.0025

            elif chosen_scenario == "structuring":
                time_delta = self.rng.randint(60, 300)
                amount_btc = round(self.rng.uniform(0.01, 0.09), 4) # micro amounts
                input_count = 1
                output_count = 1
                input_addr = generate_btc_address("smurf_in", i)
                output_addr = generate_btc_address("smurf_out", i)
                unique_counterparties = 2
                tx_size = 192
                fee_btc = 0.00015

            elif chosen_scenario == "risky_neighbor":
                time_delta = self.rng.randint(300, 1800)
                amount_btc = round(self.rng.uniform(5.0, 60.0), 4)
                input_count = 1
                output_count = 2
                input_addr = generate_btc_address("neighbor_in", i)
                output_addr = "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0" # Flagged Ransomware cluster
                unique_counterparties = 3
                tx_size = 225
                fee_btc = 0.0020

            # Realistic synthetic IP pools
            IP_POOLS = [
                ("198.51.100.", "United States", "AS64500"),
                ("8.8.8.", "United States", "AS15169"),
                ("13.225.103.", "India", "AS16509"),
                ("185.220.101.", "Germany", "AS60729"),
                ("203.0.113.", "Singapore", "AS64501"),
                ("52.84.12.", "United Kingdom", "AS16509"),
                ("133.242.10.", "Japan", "AS9370"),
                ("193.134.1.", "Switzerland", "AS13030")
            ]
            src_pool = self.rng.choice(IP_POOLS)
            dst_pool = self.rng.choice(IP_POOLS)
            src_ip = f"{src_pool[0]}{self.rng.randint(1, 254)}"
            dst_ip = f"{dst_pool[0]}{self.rng.randint(1, 254)}"
            src_port = self.rng.choice([8333, 18333, 49152, 51234, 55432])
            dst_port = 8333

            current_time = base_time + timedelta(seconds=i * 60 + time_delta)

            records.append({
                "transaction_id": txid,
                "timestamp": current_time.isoformat(),
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "geo_country": src_pool[1],
                "asn": src_pool[2],
                "input_address": input_addr,
                "output_address": output_addr,
                "amount_btc": amount_btc,
                "input_count": input_count,
                "output_count": output_count,
                "transaction_size": tx_size,
                "fee_btc": fee_btc,
                "block_height": block_height,
                "time_to_next_transaction": time_delta,
                "unique_counterparties": unique_counterparties,
                "scenario": chosen_scenario,
                "label": label
            })

        return records

    def to_csv_string(self, records: List[Dict[str, Any]]) -> str:
        fieldnames = [
            "transaction_id", "timestamp", "src_ip", "dst_ip", "src_port", "dst_port",
            "geo_country", "asn", "input_address", "output_address",
            "amount_btc", "input_count", "output_count", "transaction_size",
            "fee_btc", "block_height", "time_to_next_transaction",
            "unique_counterparties", "scenario", "label"
        ]
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        return output.getvalue()
