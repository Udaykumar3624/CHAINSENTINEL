from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, Field
from app.seed.seed_data import SEED_ALERTS

router = APIRouter()

class AlertResponseItem(BaseModel):
    id: str
    alert_code: str
    title: str
    subject_type: str
    subject_id: str
    risk_score: int
    risk_level: str
    status: str
    top_signal: str
    evidence: dict
    created_at: str

class AlertStatusUpdateRequest(BaseModel):
    status: str = Field(..., description="new, under_review, resolved, false_positive")

@router.get("", response_model=List[AlertResponseItem])
def get_alerts(
    risk_level: Optional[str] = Query(None, description="Filter by risk level: low, medium, high, critical"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: new, under_review, resolved, false_positive"),
    limit: int = Query(20, ge=1, le=100)
):
    alerts = SEED_ALERTS
    if risk_level:
        alerts = [a for a in alerts if a["risk_level"] == risk_level.lower()]
    if status_filter:
        alerts = [a for a in alerts if a["status"] == status_filter.lower()]
    
    return [AlertResponseItem(**a) for a in alerts[:limit]]

@router.get("/{alert_id}", response_model=AlertResponseItem)
def get_alert_by_id(alert_id: str):
    for alert in SEED_ALERTS:
        if alert["id"] == alert_id:
            return AlertResponseItem(**alert)
    raise HTTPException(status_code=404, detail=f"Alert with ID {alert_id} not found")

@router.patch("/{alert_id}", response_model=AlertResponseItem)
def update_alert_status(alert_id: str, payload: AlertStatusUpdateRequest):
    valid_statuses = {"new", "under_review", "resolved", "false_positive"}
    new_status = payload.status.lower()
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid alert status '{payload.status}'. Must be one of: {', '.join(sorted(valid_statuses))}"
        )

    for alert in SEED_ALERTS:
        if alert["id"] == alert_id:
            alert["status"] = new_status
            return AlertResponseItem(**alert)

    raise HTTPException(status_code=404, detail=f"Alert with ID {alert_id} not found")
