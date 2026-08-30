from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DatasetScenarioDistribution(BaseModel):
    normal: float = Field(0.4, ge=0.0, le=1.0)
    rapid_forwarding: float = Field(0.1, ge=0.0, le=1.0)
    fan_out: float = Field(0.1, ge=0.0, le=1.0)
    fan_in: float = Field(0.1, ge=0.0, le=1.0)
    peeling_chain: float = Field(0.1, ge=0.0, le=1.0)
    circular_flow: float = Field(0.05, ge=0.0, le=1.0)
    dormancy_burst: float = Field(0.05, ge=0.0, le=1.0)
    structuring: float = Field(0.05, ge=0.0, le=1.0)
    risky_neighbor: float = Field(0.05, ge=0.0, le=1.0)

class GenerateDatasetRequest(BaseModel):
    num_records: int = Field(100, ge=10, le=5000, description="Total number of transaction records to generate")
    seed: int = Field(42, ge=0, description="Random seed for reproducible dataset generation")
    scenario_distribution: Optional[DatasetScenarioDistribution] = None

class GenerateDatasetResponse(BaseModel):
    dataset_id: str
    filename: str
    num_records: int
    seed: int
    file_size_bytes: int
    created_at: str
    disclaimer: str

class ValidationErrorItem(BaseModel):
    row_index: int
    field: str
    error_type: str
    message: str
    value: Optional[str] = None

class DatasetValidationReport(BaseModel):
    is_valid: bool
    total_rows_checked: int
    error_count: int
    errors: List[ValidationErrorItem]
    warnings: List[str]

class DatasetStatsSummary(BaseModel):
    total_transactions: int
    normal_count: int
    suspicious_count: int
    total_volume_btc: float
    avg_amount_btc: float
    min_amount_btc: float
    max_amount_btc: float
    unique_inputs_count: int
    unique_outputs_count: int
    scenario_breakdown: Dict[str, int]
    label_breakdown: Dict[str, int]

class DatasetAnalysisResultItem(BaseModel):
    row_index: int
    transaction_id: str
    input_address: str
    output_address: str
    amount_btc: float
    ground_truth_scenario: str
    ground_truth_label: str
    computed_risk_score: int
    computed_risk_level: str
    top_signal: str
    timestamp: str = "2026-08-30T00:00:00Z"

class DatasetAnalysisResponse(BaseModel):
    dataset_id: str
    filename: str
    stats: DatasetStatsSummary
    validation: DatasetValidationReport
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    results: List[DatasetAnalysisResultItem]
    disclaimer: str

class ExplorerSummary(BaseModel):
    total_transactions: int
    unique_addresses: int
    total_volume_btc: float
    avg_transaction_amount_btc: float
    time_range_start: Optional[str] = None
    time_range_end: Optional[str] = None
    missing_values_count: int
    duplicate_records_count: int

class EntityExtractedFeatures(BaseModel):
    address: str
    amount_btc: float
    inputs_count: int
    outputs_count: int
    fee_btc: float
    time_delta_seconds: float
    peel_steps: int
    dormant_days: int
    micro_tx_count: int
    hop_distance: int
    tx_count_24h: int
    volume_btc_24h: float
    in_degree: int = 0
    out_degree: int = 0
    pagerank: float = 0.0
    has_cycle: bool = False

class DatasetExplorerResponse(BaseModel):
    dataset_id: str
    filename: str
    data_source_label: str = "DATA SOURCE: SYNTHETIC DATASET"
    data_source_type: str = "Synthetic" # "Synthetic", "Demo", "Live"
    summary: ExplorerSummary
    scenario_distribution: Dict[str, int]
    transactions: List[DatasetAnalysisResultItem]
    extracted_features: List[EntityExtractedFeatures]
    disclaimer: str
