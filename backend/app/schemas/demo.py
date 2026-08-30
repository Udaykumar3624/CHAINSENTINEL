from typing import List, Optional
from pydantic import BaseModel

class DemoScenarioItem(BaseModel):
    id: str
    scenario_code: str
    title: str
    risk_level: str
    expected_score: int
    subject_type: str
    subject_id: str
    description: str
    judging_story: str

class DemoScenariosResponse(BaseModel):
    scenarios: List[DemoScenarioItem]
    count: int
    mode: str = "deterministic_offline"
