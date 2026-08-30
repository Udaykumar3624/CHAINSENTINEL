import csv
import io
import re
from datetime import datetime
from typing import List, Dict, Any, Tuple
from app.schemas.dataset import DatasetValidationReport, ValidationErrorItem

REQUIRED_FIELDS = [
    "transaction_id", "timestamp", "input_address", "output_address",
    "amount_btc", "input_count", "output_count", "transaction_size",
    "fee_btc", "block_height", "time_to_next_transaction",
    "unique_counterparties", "scenario", "label"
]

BTC_ADDRESS_REGEX = re.compile(r"^(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[a-zA-Z0-9]{11,87}|tb1[a-zA-Z0-9]{11,87}|bc1q[a-z0-9_]+)$", re.IGNORECASE)

class DatasetValidator:
    @staticmethod
    def validate_csv_content(csv_content: str) -> DatasetValidationReport:
        errors: List[ValidationErrorItem] = []
        warnings: List[str] = []
        seen_txids = set()

        try:
            reader = csv.DictReader(io.StringIO(csv_content))
        except Exception as e:
            return DatasetValidationReport(
                is_valid=False,
                total_rows_checked=0,
                error_count=1,
                errors=[ValidationErrorItem(row_index=0, field="file", error_type="MALFORMED_CSV", message=f"CSV parse error: {str(e)}")],
                warnings=["File could not be parsed as valid CSV."]
            )

        if not reader.fieldnames:
            return DatasetValidationReport(
                is_valid=False,
                total_rows_checked=0,
                error_count=1,
                errors=[ValidationErrorItem(row_index=0, field="header", error_type="MISSING_HEADER", message="CSV file lacks header row.")],
                warnings=[]
            )

        # Check header missing fields
        missing_headers = [f for f in REQUIRED_FIELDS if f not in reader.fieldnames]
        if missing_headers:
            warnings.append(f"Header missing standard fields: {', '.join(missing_headers)}")

        row_index = 0
        for row in reader:
            row_index += 1

            # 1. Missing required field values
            for field in REQUIRED_FIELDS:
                val = row.get(field)
                if val is None or str(val).strip() == "":
                    errors.append(ValidationErrorItem(
                        row_index=row_index,
                        field=field,
                        error_type="MISSING_VALUE",
                        message=f"Row #{row_index}: Missing required value for column '{field}'"
                    ))

            # 2. Duplicate TxID Check
            txid = row.get("transaction_id", "").strip()
            if txid:
                if txid in seen_txids:
                    errors.append(ValidationErrorItem(
                        row_index=row_index,
                        field="transaction_id",
                        error_type="DUPLICATE_TXID",
                        message=f"Row #{row_index}: Duplicate transaction ID detected '{txid[:16]}...'",
                        value=txid
                    ))
                else:
                    seen_txids.add(txid)

            # 3. Invalid Amount Check
            amount_str = row.get("amount_btc", "").strip()
            if amount_str:
                try:
                    amount = float(amount_str)
                    if amount <= 0:
                        errors.append(ValidationErrorItem(
                            row_index=row_index,
                            field="amount_btc",
                            error_type="INVALID_AMOUNT",
                            message=f"Row #{row_index}: Amount must be positive (> 0 BTC), got {amount}",
                            value=amount_str
                        ))
                except ValueError:
                    errors.append(ValidationErrorItem(
                        row_index=row_index,
                        field="amount_btc",
                        error_type="NON_NUMERIC_AMOUNT",
                        message=f"Row #{row_index}: Amount '{amount_str}' is not a valid number",
                        value=amount_str
                    ))

            # 4. Invalid Timestamp Check
            ts_str = row.get("timestamp", "").strip()
            if ts_str:
                try:
                    # Accepts ISO format or unix float
                    if ts_str.replace('.', '', 1).isdigit():
                        float(ts_str)
                    else:
                        datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                except ValueError:
                    errors.append(ValidationErrorItem(
                        row_index=row_index,
                        field="timestamp",
                        error_type="INVALID_TIMESTAMP",
                        message=f"Row #{row_index}: Timestamp '{ts_str}' is not a valid ISO-8601 or Unix timestamp",
                        value=ts_str
                    ))

            # 5. Invalid Address Fields Check
            for addr_field in ["input_address", "output_address"]:
                addr_val = row.get(addr_field, "").strip()
                if addr_val and not BTC_ADDRESS_REGEX.match(addr_val):
                    errors.append(ValidationErrorItem(
                        row_index=row_index,
                        field=addr_field,
                        error_type="INVALID_ADDRESS_FORMAT",
                        message=f"Row #{row_index}: Invalid Bitcoin address format '{addr_val[:20]}...'",
                        value=addr_val
                    ))

        is_valid = len(errors) == 0
        return DatasetValidationReport(
            is_valid=is_valid,
            total_rows_checked=row_index,
            error_count=len(errors),
            errors=errors[:100], # Cap max error list to 100
            warnings=warnings
        )
