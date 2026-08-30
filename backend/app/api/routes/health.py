from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timezone
from app.core.config import settings
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    live_data_enabled: bool
    timestamp: str
    disclaimer: str

@router.get("/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="ok",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        live_data_enabled=settings.LIVE_DATA_ENABLED,
        timestamp=datetime.now(timezone.utc).isoformat(),
        disclaimer=RESPONSIBLE_AI_DISCLAIMER
    )
