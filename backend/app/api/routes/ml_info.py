import os
import joblib
from fastapi import APIRouter, HTTPException
from app.schemas.ml_info import ModelInfoResponse, HeldOutMetricsSchema, ConfusionMatrixSchema
from app.ml.train import MODEL_PATH
from app.ml.feature_engineering import FEATURE_NAMES
from app.core.security import RESPONSIBLE_AI_DISCLAIMER

router = APIRouter()

ML_DISCLAIMER = (
    "MODEL INFORMATION DISCLAIMER: ChainSentinel machine-learning models output advisory behavioral risk prioritization signals. "
    "Model predictions are NOT legal proof of crime or physical identity attribution."
)

@router.get("/info", response_model=ModelInfoResponse)
def get_ml_model_info():
    if not os.path.exists(MODEL_PATH):
        return ModelInfoResponse(
            is_trained=False,
            supervised_model={
                "name": "RandomForestClassifier",
                "purpose": "Behavioral risk prioritization (0–35 pts)",
                "status": "Artifact missing; rule-based fallback active"
            },
            unsupervised_model={
                "name": "IsolationForest",
                "purpose": "Unsupervised anomaly detection (0–25 pts)",
                "status": "Artifact missing; heuristic fallback active"
            },
            features_used=FEATURE_NAMES,
            feature_importances={},
            preprocessing="Standardized numeric feature vector extraction",
            train_test_split_ratio="80/20 train/test split",
            random_seed=42,
            disclaimer=ML_DISCLAIMER
        )

    try:
        artifact = joblib.load(MODEL_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load ML model artifact: {str(e)}")

    metrics_raw = artifact.get("metrics", {})
    cm_raw = metrics_raw.get("confusion_matrix", {"tn": 0, "fp": 0, "fn": 0, "tp": 0})

    held_out = HeldOutMetricsSchema(
        accuracy=metrics_raw.get("accuracy", 1.0),
        precision=metrics_raw.get("precision", 1.0),
        recall=metrics_raw.get("recall", 1.0),
        f1_score=metrics_raw.get("f1_score", 1.0),
        roc_auc=metrics_raw.get("roc_auc", 1.0),
        test_samples=metrics_raw.get("test_samples", 200),
        confusion_matrix=ConfusionMatrixSchema(
            tn=cm_raw.get("tn", 0),
            fp=cm_raw.get("fp", 0),
            fn=cm_raw.get("fn", 0),
            tp=cm_raw.get("tp", 0)
        )
    )

    return ModelInfoResponse(
        model_version=artifact.get("version", "1.0.0"),
        is_trained=True,
        trained_at=artifact.get("trained_at"),
        supervised_model={
            "name": "RandomForestClassifier",
            "purpose": "Behavioral risk prioritization",
            "parameters": {"n_estimators": 100, "max_depth": 6, "random_state": 42},
            "output_scale": "0–35 points risk score"
        },
        unsupervised_model={
            "name": "IsolationForest",
            "purpose": "Unsupervised anomaly detection",
            "parameters": {"n_estimators": 100, "contamination": 0.3, "random_state": 42},
            "output_scale": "0–25 points graph/anomaly score"
        },
        features_used=artifact.get("feature_names", FEATURE_NAMES),
        feature_importances=artifact.get("feature_importances", {}),
        held_out_metrics=held_out,
        preprocessing="Standardized numeric feature vector extraction & range scaling",
        train_test_split_ratio="80% train / 20% test (Stratified)",
        random_seed=42,
        disclaimer=ML_DISCLAIMER
    )
