import io
import csv
import statistics
import networkx as nx
from datetime import datetime
from typing import List, Dict, Any, Tuple, Set

from app.schemas.analysis import (
    CsvAnalysisBatchResponse, CsvAnalysisSummaryItem, CsvDatasetSummary
)
from app.services.analysis.analysis_service import AnalysisService
from app.services.graph.graph_service import FLAGGED_DEMO_ENTITIES
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

DATA_SOURCE_LABEL = "DATA SOURCE: USER-UPLOADED SYNTHETIC DATA"

class CsvTransactionProcessor:
    def __init__(self):
        self.analysis_service = AnalysisService()

    def process_csv_content(self, filename: str, text_content: str) -> CsvAnalysisBatchResponse:
        # 1. Parse CSV
        io_input = io.StringIO(text_content)
        reader_obj = csv.DictReader(io_input)
        if not reader_obj.fieldnames:
            raise ValueError("CSV file lacks header row.")

        headers = set(field.strip() for field in reader_obj.fieldnames)
        has_src = "source_address" in headers or "input_address" in headers
        has_dst = "destination_address" in headers or "output_address" in headers
        if not has_src or not has_dst:
            raise ValueError("Missing required CSV columns: source_address/input_address, destination_address/output_address")

        reader = list(reader_obj)
        total_records = len(reader)
        
        if total_records == 0:
            raise ValueError("Uploaded CSV file contains zero records.")

        # 2. Data Cleaning & Metrics Aggregation
        seen_txids: Set[str] = set()
        addresses_set: Set[str] = set()
        amounts: List[float] = []
        timestamps: List[datetime] = []
        missing_values_count = 0
        duplicate_records_count = 0
        scenario_dist: Dict[str, int] = {}

        cleaned_rows: List[Dict[str, Any]] = []

        for row_idx, row in enumerate(reader, 1):
            # Check missing values
            tx_hash = (row.get("tx_hash") or row.get("transaction_id") or f"tx_{row_idx}").strip()
            src_addr = (row.get("source_address") or row.get("input_address") or "").strip()
            dst_addr = (row.get("destination_address") or row.get("output_address") or "").strip()
            amt_str = str(row.get("amount_btc") or row.get("amount") or "0.0").strip()
            ts_str = str(row.get("timestamp") or "").strip()
            scen_str = str(row.get("scenario") or row.get("label") or "unlabeled").strip()

            if not src_addr or not dst_addr or not amt_str:
                missing_values_count += 1

            if tx_hash in seen_txids:
                duplicate_records_count += 1
            else:
                seen_txids.add(tx_hash)

            try:
                amt = float(amt_str)
                if amt < 0:
                    amt = 0.0
            except ValueError:
                amt = 0.0

            if src_addr:
                addresses_set.add(src_addr)
            if dst_addr:
                addresses_set.add(dst_addr)

            scenario_dist[scen_str] = scenario_dist.get(scen_str, 0) + 1
            amounts.append(amt)

            parsed_ts = None
            if ts_str:
                try:
                    parsed_ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    timestamps.append(parsed_ts)
                except ValueError:
                    pass

            cleaned_rows.append({
                "row_index": row_idx,
                "tx_hash": tx_hash,
                "source_address": src_addr,
                "destination_address": dst_addr,
                "amount_btc": amt,
                "timestamp": parsed_ts,
                "scenario": scen_str,
                "inputs_count": int(row.get("input_count") or 1),
                "outputs_count": int(row.get("output_count") or 1),
                "time_to_next": float(row.get("time_to_next_transaction") or 300.0)
            })

        # Summary calculations
        total_vol = sum(amounts)
        avg_amt = total_vol / max(1, total_records)
        median_amt = statistics.median(amounts) if amounts else 0.0

        ts_start_str = None
        ts_end_str = None
        if timestamps:
            timestamps.sort()
            ts_start_str = timestamps[0].isoformat()
            ts_end_str = timestamps[-1].isoformat()

        # 3. NetworkX Directed Graph Construction
        G = nx.DiGraph()
        for row in cleaned_rows:
            src = row["source_address"]
            dst = row["destination_address"]
            if src and dst:
                G.add_edge(src, dst, weight=row["amount_btc"], txid=row["tx_hash"])

        # Graph Metrics
        pagerank_dict = {}
        try:
            if len(G.nodes) > 0:
                pagerank_dict = nx.pagerank(G, alpha=0.85)
        except Exception:
            pagerank_dict = {n: 1.0 / max(1, len(G.nodes)) for n in G.nodes}

        # Detect Cycles in NetworkX Graph
        nodes_in_cycles: Set[str] = set()
        try:
            for cycle in nx.simple_cycles(G):
                for node in cycle:
                    nodes_in_cycles.add(node)
        except Exception:
            pass

        # 4. Feature Extraction & Risk Score Calculation per record
        results: List[CsvAnalysisSummaryItem] = []
        high_cnt = 0
        med_cnt = 0
        low_cnt = 0

        # Address-level aggregate counts
        addr_tx_counts: Dict[str, int] = {}
        addr_vol_counts: Dict[str, float] = {}
        for r in cleaned_rows:
            s = r["source_address"]
            if s:
                addr_tx_counts[s] = addr_tx_counts.get(s, 0) + 1
                addr_vol_counts[s] = addr_vol_counts.get(s, 0.0) + r["amount_btc"]

        for row in cleaned_rows:
            src = row["source_address"]
            dst = row["destination_address"]

            in_deg = G.in_degree(src) if src in G else 0
            out_deg = G.out_degree(src) if src in G else 0
            pr = round(pagerank_dict.get(src, 0.0), 4)
            has_cycle = src in nodes_in_cycles or dst in nodes_in_cycles

            # Compute shortest distance to flagged demo cluster
            min_dist = 5
            if src in G:
                for flagged_id in FLAGGED_DEMO_ENTITIES.keys():
                    if flagged_id in G:
                        try:
                            d = nx.shortest_path_length(G, source=src, target=flagged_id)
                            if d < min_dist:
                                min_dist = d
                        except (nx.NetworkXNoPath, nx.NodeNotFound):
                            pass

            # Extract derived feature vector
            tx_count_24h = addr_tx_counts.get(src, 1)
            vol_24h = addr_vol_counts.get(src, row["amount_btc"])
            val_concentration = round(row["amount_btc"] / max(0.0001, vol_24h), 2)
            unique_counterparties = len(set(G.neighbors(src))) if src in G else 1

            context = {
                "amount_btc": row["amount_btc"],
                "inputs_count": row["inputs_count"],
                "outputs_count": row["outputs_count"],
                "time_delta_seconds": row["time_to_next"],
                "peel_steps": 4 if row["scenario"] == "peeling_chain" else 1,
                "dormant_days": 210 if row["scenario"] == "dormancy_burst" else 5,
                "micro_tx_count": tx_count_24h if row["scenario"] == "structuring" or row["amount_btc"] < 0.1 else 1,
                "hop_distance": min_dist,
                "tx_count_24h": tx_count_24h,
                "volume_btc_24h": vol_24h,
                "value_concentration": val_concentration,
                "has_cycle": has_cycle,
                "cycle_length": 3 if has_cycle else 0,
                "known_flagged_neighbor": min_dist <= 1
            }

            analysis = self.analysis_service.analyze_subject("transaction", row["tx_hash"], context=context)
            analysis.data_source = DATA_SOURCE_LABEL

            if analysis.risk_level in ["high", "critical"]:
                high_cnt += 1
            elif analysis.risk_level == "medium":
                med_cnt += 1
            else:
                low_cnt += 1

            top_sig = analysis.signals[0].title if analysis.signals else "Standard Transaction Flow"

            results.append(CsvAnalysisSummaryItem(
                row_index=row["row_index"],
                tx_hash=row["tx_hash"],
                source_address=src,
                destination_address=dst,
                amount_btc=row["amount_btc"],
                risk_score=analysis.risk_score,
                risk_level=analysis.risk_level,
                top_signal=top_sig,
                in_degree=in_deg,
                out_degree=out_deg,
                pagerank=pr,
                has_cycle=has_cycle,
                hop_distance=min_dist,
                data_source_label=DATA_SOURCE_LABEL
            ))

        summary = CsvDatasetSummary(
            total_records=total_records,
            unique_addresses=len(addresses_set),
            time_range_start=ts_start_str,
            time_range_end=ts_end_str,
            total_volume_btc=round(total_vol, 4),
            avg_transaction_amount_btc=round(avg_amt, 4),
            median_transaction_amount_btc=round(median_amt, 4),
            missing_values_count=missing_values_count,
            duplicate_records_count=duplicate_records_count,
            scenario_distribution=scenario_dist
        )

        return CsvAnalysisBatchResponse(
            filename=filename,
            data_source_label=DATA_SOURCE_LABEL,
            total_rows_processed=total_records,
            summary=summary,
            high_risk_count=high_cnt,
            medium_risk_count=med_cnt,
            low_risk_count=low_cnt,
            results=results,
            disclaimer=RESPONSIBLE_AI_DISCLAIMER
        )
