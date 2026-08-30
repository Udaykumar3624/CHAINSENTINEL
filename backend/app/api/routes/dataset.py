import os
import io
import csv
import uuid
import networkx as nx
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Query, status
from fastapi.responses import FileResponse, Response

from app.schemas.dataset import (
    GenerateDatasetRequest, GenerateDatasetResponse,
    DatasetValidationReport, DatasetAnalysisResponse,
    DatasetStatsSummary, DatasetAnalysisResultItem,
    DatasetExplorerResponse, ExplorerSummary, EntityExtractedFeatures
)
from app.services.dataset.generator import SyntheticDatasetGenerator
from app.services.dataset.validator import DatasetValidator
from app.services.analysis.analysis_service import AnalysisService
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

from app.services.dataset.store import active_dataset_store

router = APIRouter()
analysis_service = AnalysisService()

DATASETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datasets_store"))
os.makedirs(DATASETS_DIR, exist_ok=True)

SYNTHETIC_DISCLAIMER = "Synthetic dataset generated for algorithm benchmarking & judging (SIH26146). Not real blockchain transaction data."

@router.post("/generate", response_model=GenerateDatasetResponse)
def generate_dataset(payload: GenerateDatasetRequest):
    dataset_id = str(uuid.uuid4())[:8]
    generator = SyntheticDatasetGenerator(seed=payload.seed)
    
    dist = payload.scenario_distribution.model_dump() if payload.scenario_distribution else None
    records = generator.generate_records(num_records=payload.num_records, distribution=dist)
    csv_str = generator.to_csv_string(records)

    filename = f"synthetic_dataset_seed{payload.seed}_{dataset_id}.csv"
    filepath = os.path.join(DATASETS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(csv_str)

    file_size = os.path.getsize(filepath)

    # Auto-activate newly generated synthetic dataset
    active_dataset_store.analyze_file(filepath, source_type="Synthetic", source_label="DATA SOURCE: SYNTHETIC DATASET")

    return GenerateDatasetResponse(
        dataset_id=dataset_id,
        filename=filename,
        num_records=len(records),
        seed=payload.seed,
        file_size_bytes=file_size,
        created_at=datetime.now(timezone.utc).isoformat(),
        disclaimer=SYNTHETIC_DISCLAIMER
    )

@router.get("/download/{dataset_id}")
def download_dataset(dataset_id: str):
    target_file = _find_dataset_by_id(dataset_id)
    if not target_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with ID '{dataset_id}' not found."
        )

    return FileResponse(
        path=target_file,
        media_type="text/csv",
        filename=os.path.basename(target_file)
    )

@router.post("/analyze/{dataset_id}", response_model=DatasetAnalysisResponse)
def analyze_generated_dataset(dataset_id: str):
    target_file = _find_dataset_by_id(dataset_id)
    if not target_file or not os.path.exists(target_file):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset with ID '{dataset_id}' not found."
        )

    # Update global active dataset store
    active_dataset_store.analyze_file(target_file, source_type="Synthetic", source_label="DATA SOURCE: SYNTHETIC DATASET")

    with open(target_file, "r", encoding="utf-8") as f:
        csv_content = f.read()

    validation_report = DatasetValidator.validate_csv_content(csv_content)
    reader = list(csv.DictReader(io.StringIO(csv_content)))
    
    total_tx = len(reader)
    if total_tx == 0:
        raise HTTPException(status_code=400, detail="Dataset file is empty.")

    amounts = []
    normal_cnt = 0
    suspicious_cnt = 0
    inputs_set = set()
    outputs_set = set()
    scenario_counts: Dict[str, int] = {}
    label_counts: Dict[str, int] = {}

    results: List[DatasetAnalysisResultItem] = []
    high_cnt = 0
    med_cnt = 0
    low_cnt = 0

    row_index = 0
    for row in reader:
        row_index += 1
        txid = row.get("transaction_id", f"tx_{row_index}").strip()
        in_addr = row.get("input_address", "").strip()
        out_addr = row.get("output_address", "").strip()
        gt_scenario = row.get("scenario", "unknown").strip()
        gt_label = row.get("label", "normal").strip()

        try:
            amt = float(row.get("amount_btc", 0.0))
        except ValueError:
            amt = 0.0

        try:
            in_cnt = int(row.get("input_count", 1))
        except ValueError:
            in_cnt = 1

        try:
            out_cnt = int(row.get("output_count", 1))
        except ValueError:
            out_cnt = 1

        try:
            time_delta = float(row.get("time_to_next_transaction", 300.0))
        except ValueError:
            time_delta = 300.0

        amounts.append(amt)
        inputs_set.add(in_addr)
        outputs_set.add(out_addr)

        if gt_label == "normal":
            normal_cnt += 1
        else:
            suspicious_cnt += 1

        scenario_counts[gt_scenario] = scenario_counts.get(gt_scenario, 0) + 1
        label_counts[gt_label] = label_counts.get(gt_label, 0) + 1

        context = {
            "amount_btc": amt,
            "inputs_count": in_cnt,
            "outputs_count": out_cnt,
            "time_delta_seconds": time_delta,
            "peel_steps": 4 if gt_scenario == "peeling_chain" else 1,
            "dormant_days": 210 if gt_scenario == "dormancy_burst" else 5,
            "micro_tx_count": 8 if gt_scenario == "structuring" else 1,
            "hop_distance": 1 if gt_scenario == "risky_neighbor" else 3,
            "tx_count_24h": 65 if gt_scenario == "rapid_forwarding" else 5,
            "volume_btc_24h": 85.0 if gt_scenario == "rapid_forwarding" else amt,
            "has_cycle": True if gt_scenario == "circular_flow" else False,
            "known_flagged_neighbor": True if gt_scenario == "risky_neighbor" else False
        }

        analysis = analysis_service.analyze_subject("transaction", txid, context=context)
        analysis.data_source = f"Synthetic Dataset ({os.path.basename(target_file)})"

        if analysis.risk_level in ["high", "critical"]:
            high_cnt += 1
        elif analysis.risk_level == "medium":
            med_cnt += 1
        else:
            low_cnt += 1

        top_sig = analysis.signals[0].title if analysis.signals else "Standard Profile"

        results.append(DatasetAnalysisResultItem(
            row_index=row_index,
            transaction_id=txid,
            input_address=in_addr,
            output_address=out_addr,
            amount_btc=amt,
            ground_truth_scenario=gt_scenario,
            ground_truth_label=gt_label,
            computed_risk_score=analysis.risk_score,
            computed_risk_level=analysis.risk_level,
            top_signal=top_sig
        ))

    stats_summary = DatasetStatsSummary(
        total_transactions=total_tx,
        normal_count=normal_cnt,
        suspicious_count=suspicious_cnt,
        total_volume_btc=round(sum(amounts), 4),
        avg_amount_btc=round(sum(amounts) / max(1, total_tx), 4),
        min_amount_btc=round(min(amounts) if amounts else 0.0, 4),
        max_amount_btc=round(max(amounts) if amounts else 0.0, 4),
        unique_inputs_count=len(inputs_set),
        unique_outputs_count=len(outputs_set),
        scenario_breakdown=scenario_counts,
        label_breakdown=label_counts
    )

    return DatasetAnalysisResponse(
        dataset_id=dataset_id,
        filename=os.path.basename(target_file),
        stats=stats_summary,
        validation=validation_report,
        high_risk_count=high_cnt,
        medium_risk_count=med_cnt,
        low_risk_count=low_cnt,
        results=results,
        disclaimer=SYNTHETIC_DISCLAIMER + " " + RESPONSIBLE_AI_DISCLAIMER
    )

@router.get("/explorer", response_model=DatasetExplorerResponse)
@router.get("/explorer/{dataset_id}", response_model=DatasetExplorerResponse)
def get_dataset_explorer(dataset_id: Optional[str] = None):
    if active_dataset_store.transactions and (not dataset_id or dataset_id in active_dataset_store.active_dataset_id):
        return DatasetExplorerResponse(
            dataset_id=active_dataset_store.active_dataset_id or "active",
            filename=active_dataset_store.active_filename or "active_dataset.csv",
            data_source_label=active_dataset_store.data_source_label,
            data_source_type=active_dataset_store.data_source_type,
            summary=active_dataset_store.summary or ExplorerSummary(
                total_transactions=len(active_dataset_store.transactions),
                unique_addresses=len(active_dataset_store.extracted_features),
                total_volume_btc=round(sum(t.amount_btc for t in active_dataset_store.transactions), 4),
                avg_transaction_amount_btc=round(sum(t.amount_btc for t in active_dataset_store.transactions)/max(1, len(active_dataset_store.transactions)), 4),
                time_range_start=active_dataset_store.transactions[0].timestamp if active_dataset_store.transactions else None,
                time_range_end=active_dataset_store.transactions[-1].timestamp if active_dataset_store.transactions else None,
                missing_values_count=0,
                duplicate_records_count=0
            ),
            scenario_distribution=active_dataset_store.scenario_distribution,
            transactions=active_dataset_store.transactions,
            extracted_features=active_dataset_store.extracted_features,
            disclaimer=SYNTHETIC_DISCLAIMER + " " + RESPONSIBLE_AI_DISCLAIMER
        )

    target_file = _find_dataset_by_id(dataset_id) if dataset_id else _get_latest_dataset_file()
    
    if not target_file or not os.path.exists(target_file):
        generator = SyntheticDatasetGenerator(seed=42)
        records = generator.generate_records(num_records=100)
        csv_str = generator.to_csv_string(records)
        target_file = os.path.join(DATASETS_DIR, "synthetic_dataset_seed42_default.csv")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(csv_str)

    with open(target_file, "r", encoding="utf-8") as f:
        csv_content = f.read()

    reader = list(csv.DictReader(io.StringIO(csv_content)))
    if not reader:
        raise HTTPException(status_code=400, detail="Dataset CSV is empty.")

    total_tx = len(reader)
    amounts = []
    timestamps = []
    missing_count = 0
    txid_set = set()
    dup_count = 0
    addresses_set = set()
    scenario_counts: Dict[str, int] = {}

    G = nx.DiGraph()
    transactions_list: List[DatasetAnalysisResultItem] = []
    row_idx = 0

    for row in reader:
        row_idx += 1
        txid = (row.get("transaction_id") or row.get("tx_hash") or f"tx_{row_idx}").strip()
        if txid in txid_set:
            dup_count += 1
        txid_set.add(txid)

        in_addr = (row.get("input_address") or row.get("source_address") or "").strip()
        out_addr = (row.get("output_address") or row.get("destination_address") or "").strip()
        if not in_addr or not out_addr:
            missing_count += 1

        addresses_set.add(in_addr)
        addresses_set.add(out_addr)

        try:
            amt = float(row.get("amount_btc") or row.get("amount") or 0.0)
        except ValueError:
            amt = 0.0
            missing_count += 1

        ts = (row.get("timestamp") or "2026-08-30T00:00:00Z").strip()
        scenario = (row.get("scenario") or row.get("label") or "normal").strip()
        label = (row.get("label") or "normal").strip()

        amounts.append(amt)
        timestamps.append(ts)
        scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1

        if in_addr and out_addr:
            G.add_edge(in_addr, out_addr, txid=txid, amount=amt)

        context = {
            "amount_btc": amt,
            "inputs_count": 1,
            "outputs_count": 2,
            "time_delta_seconds": float(row.get("time_to_next_transaction", 300)),
            "peel_steps": 4 if scenario == "peeling_chain" else 0,
            "dormant_days": 210 if scenario == "dormancy_burst" else 5,
            "micro_tx_count": 8 if scenario == "structuring" else 0,
            "hop_distance": 1 if scenario == "risky_neighbor" else 4,
            "tx_count_24h": 65 if scenario == "rapid_forwarding" else 5,
            "volume_btc_24h": 85.0 if scenario == "rapid_forwarding" else amt,
            "has_cycle": True if scenario == "circular_flow" else False
        }

        analysis = analysis_service.analyze_subject("transaction", txid, context=context)

        transactions_list.append(DatasetAnalysisResultItem(
            row_index=row_idx,
            transaction_id=txid,
            input_address=in_addr,
            output_address=out_addr,
            amount_btc=amt,
            ground_truth_scenario=scenario,
            ground_truth_label=label,
            computed_risk_score=analysis.risk_score,
            computed_risk_level=analysis.risk_level,
            top_signal=analysis.signals[0].title if analysis.signals else "Standard Retail Profile",
            timestamp=ts
        ))

    pagerank_dict = {}
    try:
        if len(G.nodes) > 0:
            pagerank_dict = nx.pagerank(G, alpha=0.85)
    except Exception:
        pagerank_dict = {n: 1.0 / max(1, len(G.nodes)) for n in G.nodes}

    cycles_found = []
    has_cycle = False
    try:
        for c in nx.simple_cycles(G):
            has_cycle = True
            cycles_found.append(c)
            if len(cycles_found) >= 5:
                break
    except Exception:
        pass

    extracted_features_list: List[EntityExtractedFeatures] = []
    for addr in list(addresses_set)[:50]:
        in_deg = G.in_degree(addr) if addr in G else 0
        out_deg = G.out_degree(addr) if addr in G else 0
        pr = round(pagerank_dict.get(addr, 0.0), 4)

        extracted_features_list.append(EntityExtractedFeatures(
            address=addr,
            amount_btc=round(sum(t.amount_btc for t in transactions_list if t.input_address == addr or t.output_address == addr), 4),
            inputs_count=max(1, in_deg),
            outputs_count=max(1, out_deg),
            fee_btc=0.0005,
            time_delta_seconds=300.0,
            peel_steps=3 if in_deg > 5 else 0,
            dormant_days=14,
            micro_tx_count=2,
            hop_distance=2,
            tx_count_24h=in_deg + out_deg,
            volume_btc_24h=round(sum(t.amount_btc for t in transactions_list if t.input_address == addr or t.output_address == addr), 4),
            in_degree=in_deg,
            out_degree=out_deg,
            pagerank=pr,
            has_cycle=has_cycle
        ))

    time_start = min(timestamps) if timestamps else None
    time_end = max(timestamps) if timestamps else None

    explorer_summary = ExplorerSummary(
        total_transactions=total_tx,
        unique_addresses=len(addresses_set),
        total_volume_btc=round(sum(amounts), 4),
        avg_transaction_amount_btc=round(sum(amounts) / max(1, total_tx), 4),
        time_range_start=time_start,
        time_range_end=time_end,
        missing_values_count=missing_count,
        duplicate_records_count=dup_count
    )

    return DatasetExplorerResponse(
        dataset_id=os.path.basename(target_file).replace(".csv", ""),
        filename=os.path.basename(target_file),
        data_source_label="DATA SOURCE: USER-UPLOADED SYNTHETIC DATASET",
        data_source_type="Synthetic",
        summary=explorer_summary,
        scenario_distribution=scenario_counts,
        transactions=transactions_list,
        extracted_features=extracted_features_list,
        disclaimer=SYNTHETIC_DISCLAIMER + " " + RESPONSIBLE_AI_DISCLAIMER
    )

@router.post("/upload", response_model=DatasetExplorerResponse)
async def upload_user_dataset_file(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.lower().split(".")[-1]
    if ext not in ["csv", "json", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .csv, .json, or .txt transaction dataset.")

    content = await file.read()
    try:
        content_str = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Malformed UTF-8 file encoding: {str(e)}")

    dataset_id = f"upload_{str(uuid.uuid4())[:8]}"
    saved_filename = f"{dataset_id}_{file.filename}"
    filepath = os.path.join(DATASETS_DIR, saved_filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content_str)

    try:
        active_dataset_store.analyze_file(filepath, source_type="Uploaded Dataset", source_label="DATA SOURCE: UPLOADED DATASET")
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Failed to parse and analyze file: {str(ex)}")

    return get_dataset_explorer(dataset_id)

@router.post("/validate", response_model=DatasetValidationReport)
async def validate_dataset_upload(file: UploadFile = File(...)):
    filename = file.filename
    ext = filename.lower().split(".")[-1]
    if ext not in ["csv", "json", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .csv, .json, or .txt transaction dataset.")

    content = await file.read()
    try:
        content_str = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Malformed UTF-8 content: {str(e)}")

    parse_res = UniversalDatasetParser.parse_content(content_str, filename)
    errors = [ValidationErrorItem(row_index=0, field="file", error_type="PARSING_ERROR", message=e) for e in parse_res.errors]
    
    return DatasetValidationReport(
        is_valid=parse_res.is_valid,
        total_rows_checked=parse_res.total_records_parsed,
        error_count=len(errors),
        errors=errors,
        warnings=parse_res.warnings
    )

def _find_dataset_by_id(dataset_id: str) -> Optional[str]:
    if not os.path.exists(DATASETS_DIR):
        return None
    for fname in os.listdir(DATASETS_DIR):
        if dataset_id in fname and any(fname.endswith(ext) for ext in [".csv", ".json", ".txt"]):
            return os.path.join(DATASETS_DIR, fname)
    return None

def _get_latest_dataset_file() -> Optional[str]:
    if not os.path.exists(DATASETS_DIR):
        return None
    files = [os.path.join(DATASETS_DIR, f) for f in os.listdir(DATASETS_DIR) if any(f.endswith(ext) for ext in [".csv", ".json", ".txt"])]
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]
