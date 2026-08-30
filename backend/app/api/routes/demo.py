from fastapi import APIRouter
from app.schemas.demo import DemoScenariosResponse, DemoScenarioItem
from app.seed.seed_data import DEMO_SCENARIOS

router = APIRouter()

@router.get("/scenarios", response_model=DemoScenariosResponse)
def get_demo_scenarios():
    items = [DemoScenarioItem(**item) for item in DEMO_SCENARIOS]
    return DemoScenariosResponse(
        scenarios=items,
        count=len(items),
        mode="deterministic_offline"
    )
