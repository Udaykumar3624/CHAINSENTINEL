from fastapi import APIRouter, Query, HTTPException, status
from app.schemas.graph import GraphResponse
from app.services.graph.graph_service import GraphService

router = APIRouter()
graph_service = GraphService()

from typing import Optional

@router.get("/{subject_type}/{subject_id}", response_model=GraphResponse)
def get_entity_graph(
    subject_type: str,
    subject_id: str,
    hops: int = Query(1, ge=1, le=2, description="Hop expansion distance (1 or 2)"),
    risk_level: str = Query("all", description="Risk level filter: all, critical, high, medium, low"),
    dataset_id: Optional[str] = Query(None, description="Optional dataset ID for real dataset graph extraction")
):
    subject_type_lower = subject_type.lower()
    if subject_type_lower not in ["address", "transaction"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subject_type. Must be 'address' or 'transaction'."
        )

    if not subject_id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="subject_id cannot be empty."
        )

    return graph_service.build_graph(
        subject_type=subject_type_lower,
        subject_id=subject_id.strip(),
        hops=hops,
        risk_filter=risk_level,
        dataset_id=dataset_id
    )
