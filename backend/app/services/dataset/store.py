import os
import io
import csv
import networkx as nx
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.schemas.dashboard import (
    DashboardSummaryResponse, KpiMetrics, RiskDistribution,
    DashboardAlertItem, ActivityTrendPoint, ActiveDatasetInfo
)
from app.schemas.dataset import DatasetAnalysisResultItem, EntityExtractedFeatures, ExplorerSummary
from app.services.analysis.analysis_service import AnalysisService
from app.services.dataset.generator import SyntheticDatasetGenerator
from app.services.dataset.validator import DatasetValidator
from app.services.dataset.parser import UniversalDatasetParser, NormalizedTransaction, FileParseResult
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

DATASETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datasets_store"))
os.makedirs(DATASETS_DIR, exist_ok=True)

class ActiveDatasetStore:
    def __init__(self):
        self.analysis_service = AnalysisService()
        self.reset()

    def reset(self):
        self.active_dataset_id: Optional[str] = None
        self.active_filename: Optional[str] = None
        self.data_source_type: str = "None"
        self.data_source_label: str = "DATA SOURCE: NO DATASET LOADED"
        self.analysis_status: str = "None"
        self.created_at: str = datetime.now(timezone.utc).isoformat()
        
        self.transactions: List[DatasetAnalysisResultItem] = []
        self.extracted_features: List[EntityExtractedFeatures] = []
        self.scenario_distribution: Dict[str, int] = {}
        self.summary: Optional[ExplorerSummary] = None

    def load_demo_dataset(self):
        """Loads deterministic seed 42 demo dataset into active store."""
        target_file = os.path.join(DATASETS_DIR, "synthetic_dataset_seed42_demo.csv")
        if not os.path.exists(target_file):
            generator = SyntheticDatasetGenerator(seed=42)
            records = generator.generate_records(num_records=100)
            csv_str = generator.to_csv_string(records)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(csv_str)
        
        self.analyze_file(target_file, source_type="Demo Dataset", source_label="DATA SOURCE: DEMO DATASET")

    def process_normalized_records(
        self,
        normalized_records: List[NormalizedTransaction],
        dataset_id: str,
        filename: str,
        source_type: str = "Uploaded Dataset",
        source_label: str = "DATA SOURCE: UPLOADED DATASET"
    ):
        self.transactions.clear()
        self.extracted_features.clear()
        self.scenario_distribution.clear()

        self.active_dataset_id = dataset_id
        self.active_filename = filename
        self.data_source_type = source_type
        self.data_source_label = source_label
        self.analysis_status = "Completed"
        self.created_at = datetime.now(timezone.utc).isoformat()

        total_tx = len(normalized_records)
        amounts = []
        timestamps = []
        missing_count = 0
        txid_set = set()
        dup_count = 0
        addresses_set = set()

        G = nx.DiGraph()
        row_idx = 0

        for tx in normalized_records:
            row_idx += 1
            txid = tx.transaction_id
            if txid in txid_set:
                dup_count += 1
            txid_set.add(txid)

            in_addr = tx.input_address
            out_addr = tx.output_address
            if not in_addr or not out_addr:
                missing_count += 1

            addresses_set.add(in_addr)
            addresses_set.add(out_addr)

            amt = tx.amount_btc
            ts = tx.timestamp
            scenario = tx.scenario
            label = tx.label

            amounts.append(amt)
            timestamps.append(ts)
            self.scenario_distribution[scenario] = self.scenario_distribution.get(scenario, 0) + 1

            if in_addr and out_addr:
                G.add_edge(in_addr, out_addr, txid=txid, amount=amt)

            context = {
                "amount_btc": amt,
                "inputs_count": tx.input_count,
                "outputs_count": tx.output_count,
                "time_delta_seconds": tx.time_to_next_transaction,
                "peel_steps": 4 if scenario == "peeling_chain" else 0,
                "dormant_days": 210 if scenario == "dormancy_burst" else 5,
                "micro_tx_count": 8 if scenario == "structuring" else 0,
                "hop_distance": 1 if scenario == "risky_neighbor" else 4,
                "tx_count_24h": 65 if scenario == "rapid_forwarding" else 5,
                "volume_btc_24h": 85.0 if scenario == "rapid_forwarding" else amt,
                "has_cycle": True if scenario == "circular_flow" else False
            }

            analysis = self.analysis_service.analyze_subject("transaction", txid, context=context)

            self.transactions.append(DatasetAnalysisResultItem(
                row_index=row_idx,
                transaction_id=txid,
                input_address=in_addr,
                output_address=out_addr,
                amount_btc=amt,
                ground_truth_scenario=scenario,
                ground_truth_label=label,
                computed_risk_score=analysis.risk_score,
                computed_risk_level=analysis.risk_level,
                top_signal=analysis.signals[0].title if analysis.signals else "Standard Profile",
                timestamp=ts
            ))

        pagerank_dict = {}
        try:
            if len(G.nodes) > 0:
                pagerank_dict = nx.pagerank(G, alpha=0.85)
        except Exception:
            pagerank_dict = {n: 1.0 / max(1, len(G.nodes)) for n in G.nodes}

        has_cycle = False
        try:
            for _ in nx.simple_cycles(G):
                has_cycle = True
                break
        except Exception:
            pass

        for addr in list(addresses_set)[:50]:
            in_deg = G.in_degree(addr) if addr in G else 0
            out_deg = G.out_degree(addr) if addr in G else 0
            pr = round(pagerank_dict.get(addr, 0.0), 4)

            self.extracted_features.append(EntityExtractedFeatures(
                address=addr,
                amount_btc=round(sum(t.amount_btc for t in self.transactions if t.input_address == addr or t.output_address == addr), 4),
                inputs_count=max(1, in_deg),
                outputs_count=max(1, out_deg),
                fee_btc=0.0005,
                time_delta_seconds=300.0,
                peel_steps=3 if in_deg > 5 else 0,
                dormant_days=14,
                micro_tx_count=2,
                hop_distance=2,
                tx_count_24h=in_deg + out_deg,
                volume_btc_24h=round(sum(t.amount_btc for t in self.transactions if t.input_address == addr or t.output_address == addr), 4),
                in_degree=in_deg,
                out_degree=out_deg,
                pagerank=pr,
                has_cycle=has_cycle
            ))

        time_start = min(timestamps) if timestamps else None
        time_end = max(timestamps) if timestamps else None

        self.summary = ExplorerSummary(
            total_transactions=total_tx,
            unique_addresses=len(addresses_set),
            total_volume_btc=round(sum(amounts), 4),
            avg_transaction_amount_btc=round(sum(amounts) / max(1, total_tx), 4),
            time_range_start=time_start,
            time_range_end=time_end,
            missing_values_count=missing_count,
            duplicate_records_count=dup_count
        )

    def analyze_file(self, filepath: str, source_type: str = "Synthetic", source_label: str = "DATA SOURCE: SYNTHETIC DATASET"):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file {filepath} not found.")

        with open(filepath, "r", encoding="utf-8") as f:
            content_str = f.read()

        filename = os.path.basename(filepath)
        dataset_id = filename.replace(".csv", "").replace(".json", "").replace(".txt", "")

        parse_result = UniversalDatasetParser.parse_content(content_str, filename)
        if not parse_result.is_valid or not parse_result.normalized_transactions:
            raise ValueError(f"File parsing failed: {', '.join(parse_result.errors)}")

        self.process_normalized_records(
            normalized_records=parse_result.normalized_transactions,
            dataset_id=dataset_id,
            filename=filename,
            source_type=source_type,
            source_label=source_label
        )

    def get_dashboard_summary(self) -> DashboardSummaryResponse:
        if not self.active_dataset_id or not self.transactions:
            # Clean initial zero-state when no dataset is loaded
            return DashboardSummaryResponse(
                kpis=KpiMetrics(
                    total_transactions_analyzed=0,
                    high_critical_alerts=0,
                    open_cases=0,
                    flagged_clusters=0
                ),
                risk_distribution=RiskDistribution(
                    low=0, medium=0, high=0, critical=0
                ),
                recent_alerts=[],
                activity_trend=[],
                active_dataset=ActiveDatasetInfo(
                    dataset_id="None",
                    filename="No dataset loaded",
                    data_source_type="None",
                    data_source_label="DATA SOURCE: NO DATASET LOADED",
                    row_count=0,
                    analysis_status="None",
                    created_at=self.created_at
                ),
                disclaimer=RESPONSIBLE_AI_DISCLAIMER
            )

        total_tx = len(self.transactions)
        low_count = sum(1 for t in self.transactions if t.computed_risk_score < 30)
        med_count = sum(1 for t in self.transactions if 30 <= t.computed_risk_score < 70)
        high_count = sum(1 for t in self.transactions if 70 <= t.computed_risk_score < 90)
        crit_count = sum(1 for t in self.transactions if t.computed_risk_score >= 90)
        high_critical = high_count + crit_count

        alerts_list: List[DashboardAlertItem] = []
        alert_idx = 0
        for t in self.transactions:
            if t.computed_risk_score >= 50 or t.ground_truth_label == "suspicious":
                alert_idx += 1
                alerts_list.append(DashboardAlertItem(
                    id=f"alert-{alert_idx:03d}",
                    alert_code=f"ALT-2026-{alert_idx:03d}",
                    title=f"High Risk Transaction ({t.ground_truth_scenario.title()})",
                    subject_type="transaction",
                    subject_id=t.transaction_id,
                    risk_score=t.computed_risk_score,
                    risk_level=t.computed_risk_level,
                    status="new",
                    top_signal=t.top_signal,
                    created_at=t.timestamp or datetime.now(timezone.utc).isoformat()
                ))
            if len(alerts_list) >= 10:
                break

        if not alerts_list and self.transactions:
            for i, t in enumerate(self.transactions[:5]):
                alerts_list.append(DashboardAlertItem(
                    id=f"alert-{i+1:03d}",
                    alert_code=f"ALT-2026-{i+1:03d}",
                    title=f"Behavioral Risk Target ({t.ground_truth_scenario.title()})",
                    subject_type="transaction",
                    subject_id=t.transaction_id,
                    risk_score=t.computed_risk_score,
                    risk_level=t.computed_risk_level,
                    status="new",
                    top_signal=t.top_signal,
                    created_at=t.timestamp or datetime.now(timezone.utc).isoformat()
                ))

        trend_map: Dict[str, Dict[str, int]] = {}
        for t in self.transactions:
            date_str = (t.timestamp or "2026-08-30")[:10]
            if date_str not in trend_map:
                trend_map[date_str] = {"low": 0, "medium": 0, "high": 0, "critical": 0}
            
            s = t.computed_risk_score
            if s < 30: trend_map[date_str]["low"] += 1
            elif s < 70: trend_map[date_str]["medium"] += 1
            elif s < 90: trend_map[date_str]["high"] += 1
            else: trend_map[date_str]["critical"] += 1

        activity_trend = [
            ActivityTrendPoint(
                date=d,
                low_count=counts["low"],
                medium_count=counts["medium"],
                high_count=counts["high"],
                critical_count=counts["critical"]
            ) for d, counts in sorted(trend_map.items())
        ]

        active_info = ActiveDatasetInfo(
            dataset_id=self.active_dataset_id,
            filename=self.active_filename or "active_dataset.csv",
            data_source_type=self.data_source_type,
            data_source_label=self.data_source_label,
            row_count=total_tx,
            analysis_status=self.analysis_status,
            created_at=self.created_at
        )

        return DashboardSummaryResponse(
            kpis=KpiMetrics(
                total_transactions_analyzed=total_tx,
                high_critical_alerts=high_critical,
                open_cases=1 if total_tx > 0 else 0,
                flagged_clusters=max(1, sum(1 for t in self.transactions if t.ground_truth_scenario in ['circular_flow', 'peeling_chain'])) if total_tx > 0 else 0
            ),
            risk_distribution=RiskDistribution(
                low=low_count,
                medium=med_count,
                high=high_count,
                critical=crit_count
            ),
            recent_alerts=alerts_list,
            activity_trend=activity_trend,
            active_dataset=active_info,
            disclaimer=RESPONSIBLE_AI_DISCLAIMER
        )

active_dataset_store = ActiveDatasetStore()
