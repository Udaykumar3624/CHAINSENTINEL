from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AddressAnalysisRequest(BaseModel):
    address: str = Field(..., description="Bitcoin address to analyze (Legacy, SegWit, or Taproot)")

class TransactionAnalysisRequest(BaseModel):
    txid: str = Field(..., description="64-character Bitcoin transaction ID")

class SignalItem(BaseModel):
    code: str
    title: str
    severity: str # low, medium, high, critical
    score_contribution: int
    explanation: str
    observed_values: Dict[str, Any]
    recommended_review_step: str

class RiskDecomposition(BaseModel):
    rule_score: float = Field(..., ge=0, le=40)
    ml_score: float = Field(..., ge=0, le=35)
    graph_score: float = Field(..., ge=0, le=25)

class AnalysisResultResponse(BaseModel):
    subject_type: str # address, transaction, csv_batch
    subject_id: str
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str # low, medium, high, critical
    composite_risk_score: int = Field(..., ge=0, le=100)
    risk_category: str # LOW, MEDIUM, HIGH, CRITICAL
    rule_score: float = Field(..., ge=0, le=40)
    ml_score: float = Field(..., ge=0, le=35)
    graph_score: float = Field(..., ge=0, le=25)
    confidence: float = Field(..., ge=0.0, le=1.0)
    score_decomposition: RiskDecomposition
    triggered_indicators: List[str]
    feature_values: Dict[str, Any]
    evidence: List[SignalItem]
    signals: List[SignalItem] # Kept for backward compatibility
    recommended_action: str
    data_source: str # demo, uploaded_csv, live_api
    is_ml_fallback: bool = False
    network_context: Optional[Dict[str, Any]] = None
    disclaimer: str
    analyzed_at: str

class CsvDatasetSummary(BaseModel):
    total_records: int
    unique_addresses: int
    time_range_start: Optional[str] = None
    time_range_end: Optional[str] = None
    total_volume_btc: float
    avg_transaction_amount_btc: float
    median_transaction_amount_btc: float
    missing_values_count: int
    duplicate_records_count: int
    scenario_distribution: Dict[str, int]

class CsvAnalysisSummaryItem(BaseModel):
    row_index: int
    tx_hash: str
    source_address: str
    destination_address: str
    amount_btc: float
    risk_score: int
    risk_level: str
    top_signal: str
    in_degree: int = 0
    out_degree: int = 0
    pagerank: float = 0.0
    has_cycle: bool = False
    hop_distance: int = 5
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    geo_country: Optional[str] = None
    asn: Optional[str] = None
    data_source_label: str = "DATA SOURCE: USER-UPLOADED SYNTHETIC DATA"

class CsvAnalysisBatchResponse(BaseModel):
    filename: str
    data_source_label: str = "DATA SOURCE: USER-UPLOADED SYNTHETIC DATA"
    total_rows_processed: int
    summary: CsvDatasetSummary
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    results: List[CsvAnalysisSummaryItem]
    disclaimer: str
