from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class KpiMetrics(BaseModel):
    total_transactions_analyzed: int = Field(..., description="Total Bitcoin transactions processed")
    high_critical_alerts: int = Field(..., description="Active high and critical risk alerts")
    open_cases: int = Field(..., description="Open investigative cases")
    flagged_clusters: int = Field(..., description="Identified high-risk network clusters")

class RiskDistribution(BaseModel):
    low: int = Field(..., description="Count of low risk entities (0-29)")
    medium: int = Field(..., description="Count of medium risk entities (30-69)")
    high: int = Field(..., description="Count of high risk entities (70-89)")
    critical: int = Field(..., description="Count of critical risk entities (90-100)")

class DashboardAlertItem(BaseModel):
    id: str
    alert_code: str
    title: str
    subject_type: str
    subject_id: str
    risk_score: int
    risk_level: str
    status: str
    top_signal: str
    created_at: str

class ActivityTrendPoint(BaseModel):
    date: str
    low_count: int
    medium_count: int
    high_count: int
    critical_count: int

class ActiveDatasetInfo(BaseModel):
    dataset_id: str
    filename: str
    data_source_type: str
    data_source_label: str
    row_count: int
    analysis_status: str
    created_at: str

class DashboardSummaryResponse(BaseModel):
    kpis: KpiMetrics
    risk_distribution: RiskDistribution
    recent_alerts: List[DashboardAlertItem]
    activity_trend: List[ActivityTrendPoint]
    active_dataset: Optional[ActiveDatasetInfo] = None
    disclaimer: str
