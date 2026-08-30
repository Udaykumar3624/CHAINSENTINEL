from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ConfusionMatrixSchema(BaseModel):
    tn: int
    fp: int
    fn: int
    tp: int

class HeldOutMetricsSchema(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    test_samples: int
    confusion_matrix: ConfusionMatrixSchema

class ModelInfoResponse(BaseModel):
    model_name: str = "RandomForestClassifier & IsolationForest Baseline"
    model_version: str = "1.0.0"
    is_trained: bool
    trained_at: Optional[str] = None
    supervised_model: Dict[str, Any]
    unsupervised_model: Dict[str, Any]
    features_used: List[str]
    feature_importances: Dict[str, float]
    held_out_metrics: Optional[HeldOutMetricsSchema] = None
    preprocessing: str
    train_test_split_ratio: str
    random_seed: int
    disclaimer: str
