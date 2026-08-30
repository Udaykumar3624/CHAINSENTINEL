import os
import sys
import datetime
import numpy as np
import joblib
from typing import Dict, Any, Tuple
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
)

# Ensure backend root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.ml.feature_engineering import FEATURE_NAMES, extract_feature_vector

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "risk_model.joblib")

def generate_synthetic_dataset(num_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """Generate reproducible synthetic training dataset modeled after Bitcoin risk scenarios."""
    np.random.seed(42)
    X = []
    y = []

    for _ in range(num_samples):
        is_risky = np.random.choice([0, 1], p=[0.7, 0.3])
        if is_risky:
            amount_btc = np.random.exponential(scale=15.0) + 0.1
            inputs_count = np.random.choice([1, 2, 12, 25])
            outputs_count = np.random.choice([1, 2, 28, 50])
            fee_btc = np.random.uniform(0.001, 0.05)
            time_delta_seconds = np.random.uniform(10, 300)
            peel_steps = np.random.choice([0, 3, 5, 8])
            dormant_days = np.random.choice([0, 190, 365])
            micro_tx_count = np.random.choice([0, 6, 12])
            hop_distance = np.random.choice([1, 2, 5])
            tx_count_24h = np.random.randint(20, 150)
            volume_btc_24h = np.random.uniform(30.0, 300.0)
        else:
            amount_btc = np.random.uniform(0.01, 2.5)
            inputs_count = np.random.choice([1, 2])
            outputs_count = np.random.choice([1, 2])
            fee_btc = np.random.uniform(0.0001, 0.001)
            time_delta_seconds = np.random.uniform(1800, 86400)
            peel_steps = 0
            dormant_days = np.random.randint(0, 30)
            micro_tx_count = np.random.randint(0, 2)
            hop_distance = np.random.choice([4, 5, 6])
            tx_count_24h = np.random.randint(1, 15)
            volume_btc_24h = np.random.uniform(0.1, 5.0)

        feature_dict = {
            "amount_btc": amount_btc,
            "inputs_count": inputs_count,
            "outputs_count": outputs_count,
            "fee_btc": fee_btc,
            "time_delta_seconds": time_delta_seconds,
            "peel_steps": peel_steps,
            "dormant_days": dormant_days,
            "micro_tx_count": micro_tx_count,
            "hop_distance": hop_distance,
            "tx_count_24h": tx_count_24h,
            "volume_btc_24h": volume_btc_24h
        }
        X.append(extract_feature_vector(feature_dict))
        y.append(is_risky)

    return np.array(X), np.array(y)

def train_and_save_model() -> Dict[str, Any]:
    print("Generating synthetic dataset (1,000 samples)...")
    X, y = generate_synthetic_dataset(num_samples=1000)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training RandomForestClassifier and IsolationForest models...")
    rf_clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    rf_clf.fit(X_train, y_train)

    iso_forest = IsolationForest(n_estimators=100, contamination=0.3, random_state=42)
    iso_forest.fit(X_train)

    # Calculate actual held-out metrics
    y_pred = rf_clf.predict(X_test)
    y_prob = rf_clf.predict_proba(X_test)[:, 1]

    accuracy = float(accuracy_score(y_test, y_pred))
    precision = float(precision_score(y_test, y_pred))
    recall = float(recall_score(y_test, y_pred))
    f1 = float(f1_score(y_test, y_pred))
    roc_auc = float(roc_auc_score(y_test, y_prob))

    # Confusion matrix computation
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = [int(x) for x in cm.ravel()]

    # Feature importance extraction
    feat_importances = dict(zip(FEATURE_NAMES, [round(float(imp), 4) for imp in rf_clf.feature_importances_]))

    print(f"Held-Out Evaluation Metrics:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"  ROC-AUC:   {roc_auc:.4f}")
    print(f"  Confusion Matrix: TN={tn}, FP={fp}, FN={fn}, TP={tp}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    model_artifact = {
        "rf_model": rf_clf,
        "iso_model": iso_forest,
        "feature_names": FEATURE_NAMES,
        "feature_importances": feat_importances,
        "version": "1.0.0",
        "trained_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "metrics": {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "roc_auc": round(roc_auc, 4),
            "test_samples": len(y_test),
            "confusion_matrix": {
                "tn": tn,
                "fp": fp,
                "fn": fn,
                "tp": tp
            }
        }
    }

    joblib.dump(model_artifact, MODEL_PATH)
    print(f"Model successfully saved to {MODEL_PATH}")
    return model_artifact["metrics"]

if __name__ == "__main__":
    train_and_save_model()
