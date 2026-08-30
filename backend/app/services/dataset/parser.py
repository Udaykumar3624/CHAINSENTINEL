import json
import csv
import io
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional
from pydantic import BaseModel, Field

FIELD_MAPPINGS: Dict[str, List[str]] = {
    "transaction_id": ["transaction_id", "txid", "hash", "tx_hash", "id"],
    "timestamp": ["timestamp", "time", "datetime", "created_at", "date"],
    "input_address": ["input_address", "from_address", "sender", "source_address", "input_addr", "inputs"],
    "output_address": ["output_address", "to_address", "receiver", "destination_address", "output_addr", "outputs"],
    "amount_btc": ["amount_btc", "amount", "input_value_btc", "output_value_btc", "value_btc", "value", "btc"],
    "input_count": ["input_count", "inputs_count", "in_cnt", "num_inputs"],
    "output_count": ["output_count", "outputs_count", "out_cnt", "num_outputs"],
    "fee_btc": ["fee_btc", "fee", "fees"],
    "block_height": ["block_height", "block", "height"],
    "time_to_next_transaction": ["time_to_next_transaction", "time_delta", "forwarding_delay", "delay_seconds"],
    "scenario": ["scenario", "behavioral_scenario", "pattern", "type"],
    "label": ["label", "risk_label", "category", "target"]
}

UNSECURE_KEYS = ["private_key", "secret", "seed_phrase", "mnemonic", "password", "privkey"]

class NormalizedTransaction(BaseModel):
    transaction_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    input_address: str
    output_address: str
    amount_btc: float = 0.0
    input_count: int = 1
    output_count: int = 2
    fee_btc: float = 0.0005
    block_height: int = 895200
    time_to_next_transaction: float = 300.0
    scenario: str = "normal"
    label: str = "normal"

class FileParseResult(BaseModel):
    file_type: str
    total_records_parsed: int
    normalized_transactions: List[NormalizedTransaction]
    errors: List[str]
    warnings: List[str]
    is_valid: bool

class UniversalDatasetParser:
    @staticmethod
    def _map_field(row: Dict[str, Any], canonical_field: str) -> Optional[Any]:
        candidates = FIELD_MAPPINGS.get(canonical_field, [canonical_field])
        for key in row.keys():
            normalized_key = key.strip().lower()
            if normalized_key in candidates:
                val = row[key]
                if val is not None and str(val).strip() != "":
                    return val
        return None

    @staticmethod
    def _normalize_dict_record(row: Dict[str, Any], row_idx: int) -> Tuple[Optional[NormalizedTransaction], List[str]]:
        warnings: List[str] = []

        # Security check
        for k in row.keys():
            if any(unsec in k.lower() for unsec in UNSECURE_KEYS):
                raise ValueError(f"SECURITY ALERT: Record #{row_idx} contains credentials field '{k}'. Private keys must NEVER be uploaded!")

        txid = UniversalDatasetParser._map_field(row, "transaction_id") or f"tx_{row_idx:04d}"
        in_addr = UniversalDatasetParser._map_field(row, "input_address") or f"bc1qsender_{row_idx:04d}"
        out_addr = UniversalDatasetParser._map_field(row, "output_address") or f"bc1qreceiver_{row_idx:04d}"
        
        raw_amt = UniversalDatasetParser._map_field(row, "amount_btc")
        try:
            amt = float(raw_amt) if raw_amt is not None else 1.0
            if amt < 0:
                warnings.append(f"Row #{row_idx}: Negative amount {amt} converted to 0.0 BTC.")
                amt = 0.0
        except ValueError:
            warnings.append(f"Row #{row_idx}: Non-numeric amount '{raw_amt}', default 0.0 BTC used.")
            amt = 0.0

        raw_ts = UniversalDatasetParser._map_field(row, "timestamp")
        ts = str(raw_ts).strip() if raw_ts else datetime.now(timezone.utc).isoformat()

        scenario = str(UniversalDatasetParser._map_field(row, "scenario") or "normal").strip().lower()
        label = str(UniversalDatasetParser._map_field(row, "label") or "normal").strip().lower()

        try:
            in_cnt = int(UniversalDatasetParser._map_field(row, "input_count") or 1)
        except ValueError:
            in_cnt = 1

        try:
            out_cnt = int(UniversalDatasetParser._map_field(row, "output_count") or 2)
        except ValueError:
            out_cnt = 2

        try:
            time_delta = float(UniversalDatasetParser._map_field(row, "time_to_next_transaction") or 300.0)
        except ValueError:
            time_delta = 300.0

        norm_tx = NormalizedTransaction(
            transaction_id=str(txid).strip(),
            timestamp=ts,
            input_address=str(in_addr).strip(),
            output_address=str(out_addr).strip(),
            amount_btc=amt,
            input_count=in_cnt,
            output_count=out_cnt,
            fee_btc=0.0005,
            block_height=895200,
            time_to_next_transaction=time_delta,
            scenario=scenario,
            label=label
        )
        return norm_tx, warnings

    @classmethod
    def parse_content(cls, content_str: str, filename: str) -> FileParseResult:
        errors: List[str] = []
        warnings: List[str] = []
        normalized: List[NormalizedTransaction] = []
        ext = filename.lower().split('.')[-1]

        if not content_str.strip():
            return FileParseResult(
                file_type=ext.upper(),
                total_records_parsed=0,
                normalized_transactions=[],
                errors=["Dataset file is completely empty."],
                warnings=[],
                is_valid=False
            )

        if ext == "json":
            return cls._parse_json(content_str)
        elif ext == "txt":
            return cls._parse_txt(content_str)
        else: # Default CSV
            return cls._parse_csv(content_str)

    @classmethod
    def _parse_csv(cls, content_str: str) -> FileParseResult:
        errors: List[str] = []
        warnings: List[str] = []
        normalized: List[NormalizedTransaction] = []

        try:
            reader = list(csv.DictReader(io.StringIO(content_str)))
        except Exception as e:
            return FileParseResult(
                file_type="CSV",
                total_records_parsed=0,
                normalized_transactions=[],
                errors=[f"CSV parsing error: {str(e)}"],
                warnings=[],
                is_valid=False
            )

        if not reader:
            return FileParseResult(
                file_type="CSV",
                total_records_parsed=0,
                normalized_transactions=[],
                errors=["CSV file contains no data rows."],
                warnings=[],
                is_valid=False
            )

        for idx, row in enumerate(reader, 1):
            try:
                tx, row_warns = cls._normalize_dict_record(row, idx)
                if tx:
                    normalized.append(tx)
                warnings.extend(row_warns)
            except Exception as ex:
                errors.append(str(ex))

        return FileParseResult(
            file_type="CSV",
            total_records_parsed=len(normalized),
            normalized_transactions=normalized,
            errors=errors,
            warnings=warnings,
            is_valid=len(errors) == 0 and len(normalized) > 0
        )

    @classmethod
    def _parse_json(cls, content_str: str) -> FileParseResult:
        errors: List[str] = []
        warnings: List[str] = []
        normalized: List[NormalizedTransaction] = []

        try:
            data = json.loads(content_str)
        except Exception as e:
            return FileParseResult(
                file_type="JSON",
                total_records_parsed=0,
                normalized_transactions=[],
                errors=[f"JSON syntax error: {str(e)}"],
                warnings=[],
                is_valid=False
            )

        records_list: List[Dict[str, Any]] = []
        if isinstance(data, list):
            records_list = data
        elif isinstance(data, dict):
            for k in ["transactions", "data", "records", "items"]:
                if k in data and isinstance(data[k], list):
                    records_list = data[k]
                    break
            if not records_list:
                records_list = [data]

        for idx, item in enumerate(records_list, 1):
            if not isinstance(item, dict):
                warnings.append(f"JSON Item #{idx} is not an object, skipping.")
                continue
            try:
                tx, row_warns = cls._normalize_dict_record(item, idx)
                if tx:
                    normalized.append(tx)
                warnings.extend(row_warns)
            except Exception as ex:
                errors.append(str(ex))

        return FileParseResult(
            file_type="JSON",
            total_records_parsed=len(normalized),
            normalized_transactions=normalized,
            errors=errors,
            warnings=warnings,
            is_valid=len(errors) == 0 and len(normalized) > 0
        )

    @classmethod
    def _parse_txt(cls, content_str: str) -> FileParseResult:
        errors: List[str] = []
        warnings: List[str] = []
        normalized: List[NormalizedTransaction] = []

        lines = [line.strip() for line in content_str.splitlines() if line.strip()]
        if not lines:
            return FileParseResult(
                file_type="TXT",
                total_records_parsed=0,
                normalized_transactions=[],
                errors=["TXT file contains no text lines."],
                warnings=[],
                is_valid=False
            )

        # Detect delimiter (comma, tab, pipe)
        first_line = lines[0]
        delimiter = ","
        if "\t" in first_line: delimiter = "\t"
        elif "|" in first_line: delimiter = "|"

        # Check if first line is a header
        header_keys = [k.strip().lower() for k in first_line.split(delimiter)]
        has_header = any(hk in ["transaction_id", "txid", "timestamp", "input_address", "sender", "amount_btc", "amount"] for hk in header_keys)

        data_lines = lines[1:] if has_header else lines

        for idx, line in enumerate(data_lines, 1):
            parts = [p.strip() for p in line.split(delimiter)]
            record_dict: Dict[str, Any] = {}

            if has_header:
                for h, p in zip(header_keys, parts):
                    record_dict[h] = p
            else:
                # Fallback positional fields: txid, timestamp, input_address, output_address, amount_btc, scenario, label
                if len(parts) >= 5:
                    record_dict["transaction_id"] = parts[0]
                    record_dict["timestamp"] = parts[1]
                    record_dict["input_address"] = parts[2]
                    record_dict["output_address"] = parts[3]
                    record_dict["amount_btc"] = parts[4]
                    if len(parts) >= 6: record_dict["scenario"] = parts[5]
                    if len(parts) >= 7: record_dict["label"] = parts[6]
                else:
                    warnings.append(f"TXT Line #{idx} has insufficient columns ({len(parts)}), skipped.")
                    continue

            try:
                tx, row_warns = cls._normalize_dict_record(record_dict, idx)
                if tx:
                    normalized.append(tx)
                warnings.extend(row_warns)
            except Exception as ex:
                errors.append(str(ex))

        return FileParseResult(
            file_type="TXT",
            total_records_parsed=len(normalized),
            normalized_transactions=normalized,
            errors=errors,
            warnings=warnings,
            is_valid=len(errors) == 0 and len(normalized) > 0
        )
