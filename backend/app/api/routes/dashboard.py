from fastapi import APIRouter
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dataset.store import active_dataset_store

router = APIRouter()

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary():
    return active_dataset_store.get_dashboard_summary()

@router.post("/reset", response_model=DashboardSummaryResponse)
def reset_active_dataset():
    active_dataset_store.reset()
    return active_dataset_store.get_dashboard_summary()

@router.post("/load-demo", response_model=DashboardSummaryResponse)
def load_demo_dataset():
    active_dataset_store.load_demo_dataset()
    return active_dataset_store.get_dashboard_summary()
