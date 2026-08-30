import os
import joblib
import numpy as np
from typing import Dict, Any, List, Optional
from app.ml.feature_engineering import FEATURE_NAMES, extract_feature_vector

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "risk_model.joblib")

class MLInferenceEngine:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or MODEL_PATH
        self.ml_available = False
        self.rf_model = None
        self.iso_model = None
        self.feature_names = FEATURE_NAMES
        self.metadata = {}
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                artifact = joblib.load(self.model_path)
                self.rf_model = artifact.get("rf_model")
                self.iso_model = artifact.get("iso_model")
                self.feature_names = artifact.get("feature_names", FEATURE_NAMES)
                self.metadata = {
                    "version": artifact.get("version", "1.0.0"),
                    "trained_at": artifact.get("trained_at"),
                    "metrics": artifact.get("metrics", {})
                }
                if self.rf_model is not None and self.iso_model is not None:
                    self.ml_available = True
            except Exception as e:
                self.ml_available = False
                self.metadata["error"] = str(e)
        else:
            self.ml_available = False

    def predict(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform ML inference with automatic rule-based fallback if model unavailable."""
        if not self.ml_available:
            return {
                "ml_available": False,
                "ml_score": 0.0,
                "graph_anomaly_score": 0.0,
                "top_features": [],
                "message": "ML model unavailable; rule-based analysis used.",
                "metrics": {}
            }

        vector = np.array([extract_feature_vector(context)])

        # 1. Supervised Risk Score (0-35 points)
        prob = float(self.rf_model.predict_proba(vector)[0, 1])
        ml_score = round(prob * 35.0, 2)

        # 2. Anomaly Score (0-25 points)
        raw_anomaly = float(self.iso_model.decision_function(vector)[0])
        # IsolationForest decision_function: lower means more anomalous
        # Map raw_anomaly (-0.5 to 0.5) inversely to 0-25 range
        norm_anomaly = max(0.0, min(1.0, 0.5 - raw_anomaly))
        anomaly_score = round(norm_anomaly * 25.0, 2)

        # Top 3 feature importances
        feature_importances = self.rf_model.feature_importances_
        top_indices = np.argsort(feature_importances)[::-1][:3]
        top_features = [
            {
                "feature": self.feature_names[idx],
                "importance": float(round(feature_importances[idx], 4)),
                "observed_value": float(vector[0][idx])
            }
            for idx in top_indices
        ]

        return {
            "ml_available": True,
            "ml_score": ml_score,
            "graph_anomaly_score": anomaly_score,
            "top_features": top_features,
            "message": "RandomForest & IsolationForest inference complete.",
            "metrics": self.metadata.get("metrics", {})
        }
