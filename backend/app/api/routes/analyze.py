import io
import csv
from typing import List, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Request, status
from app.schemas.analysis import (
    AddressAnalysisRequest, TransactionAnalysisRequest, AnalysisResultResponse,
    CsvAnalysisBatchResponse, CsvAnalysisSummaryItem
)
from app.services.analysis.analysis_service import AnalysisService
from app.services.providers.factory import get_blockchain_provider
from app.core.rate_limiter import analysis_rate_limiter
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

router = APIRouter()
analysis_service = AnalysisService()

MAX_CSV_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_CSV_ROWS = 10000
ALLOWED_COLUMNS = {"tx_hash", "source_address", "destination_address", "amount_btc", "timestamp"}

@router.post("/address", response_model=AnalysisResultResponse)
def analyze_address(payload: AddressAnalysisRequest, request: Request):
    analysis_rate_limiter.check_rate_limit(request)
    address = payload.address.strip()
    if not address or len(address) < 14:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid Bitcoin address format. Address must be a valid Bitcoin Legacy, SegWit, or Taproot address."
        )
    return analysis_service.analyze_address(address)

@router.post("/transaction", response_model=AnalysisResultResponse)
def analyze_transaction(payload: TransactionAnalysisRequest, request: Request):
    analysis_rate_limiter.check_rate_limit(request)
    txid = payload.txid.strip()
    if not txid or len(txid) < 32:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid Bitcoin transaction ID format. Must be a valid 64-character hex TxID."
        )
    return analysis_service.analyze_transaction(txid)

@router.get("/live/address/{address}")
async def get_live_address_data(address: str, request: Request):
    analysis_rate_limiter.check_rate_limit(request)
    provider = get_blockchain_provider(force_live=True)
    return await provider.get_address(address)

@router.get("/live/tx/{txid}")
async def get_live_transaction_data(txid: str, request: Request):
    analysis_rate_limiter.check_rate_limit(request)
    provider = get_blockchain_provider(force_live=True)
    return await provider.get_transaction(txid)

@router.get("/live/address/{address}/txs")
async def get_live_address_transactions_data(address: str, request: Request, limit: int = 20):
    analysis_rate_limiter.check_rate_limit(request)
    provider = get_blockchain_provider(force_live=True)
    return await provider.get_address_transactions(address, limit=limit)

from app.services.analysis.csv_processor import CsvTransactionProcessor

csv_processor = CsvTransactionProcessor()

@router.post("/csv", response_model=CsvAnalysisBatchResponse)
async def analyze_csv(request: Request, file: UploadFile = File(...)):
    analysis_rate_limiter.check_rate_limit(request)
    # 1. Validate file extension
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file extension. Only .csv files are supported."
        )

    # 2. Read file content and validate size (10 MB max)
    content = await file.read()
    if len(content) > MAX_CSV_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 10 MB maximum limit."
        )

    if len(content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded CSV file is empty."
        )

    try:
        text_content = content.decode('utf-8')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Malformed UTF-8 CSV content: {str(e)}"
        )

    try:
        return csv_processor.process_csv_content(file.filename, text_content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process CSV transaction batch: {str(e)}"
        )
