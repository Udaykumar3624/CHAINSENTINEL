# ChainSentinel Model Card: Bitcoin Transaction Risk Classifier (v1.0.0)

**Problem Statement**: SIH26146 — AI-Powered Monitoring & Analysis of Bitcoin Transaction Traffic  
**Model Architecture**: Dual Baseline (`RandomForestClassifier` + `IsolationForest`)  
**Artifact Path**: `backend/app/ml/models/risk_model.joblib`  
**License / Mode**: Read-only, Explainable Prioritization Signal  

---

## 1. Intended Use

ChainSentinel is an **explainable, read-only decision-support platform** designed to assist cybercrime analysts, financial intelligence units, and compliance officers in prioritizing potentially suspicious Bitcoin transaction behavior.

### Primary Intended Uses
- Prioritizing high-volume transaction feeds for human analyst review.
- Identifying structural graph anomalies (peeling chains, fan-out dispersal, fan-in consolidation, circular loops).
- Visualizing topological risk proximity to known flagged clusters.

---

## 2. Non-Use & Prohibited Use Cases

> [!CAUTION]
> **STRICT PROHIBITION**:
> 1. **No Person Identification**: This model operates strictly on pseudonymized Bitcoin addresses and transaction hashes. It cannot identify real-world individuals, IP addresses, or legal names.
> 2. **No Legal Proof of Guilt**: Risk scores (0–100) are prioritization heuristics, not legal evidence or proof of unlawful activity.
> 3. **No Automated Asset Freezing**: Model outputs must never be used to automatically block, drain, or confiscate funds without human oversight.

---

## 3. Training & Evaluation Methodology

- **Dataset**: 1,000 synthetic transaction contexts derived from deterministic Smart India Hackathon 2026 judging scenarios.
- **Train/Test Split**: 80% Training (800 samples) / 20% Held-Out Test (200 samples).
- **Features (11 Numeric Indicators)**: `amount_btc`, `inputs_count`, `outputs_count`, `fee_btc`, `time_delta_seconds`, `peel_steps`, `dormant_days`, `micro_tx_count`, `hop_distance`, `tx_count_24h`, `volume_btc_24h`.

### Held-Out Evaluation Metrics (Calculated on 200 Test Samples)
- **Accuracy**: `1.0000` (100.0%)
- **Precision**: `1.0000` (100.0%)
- **Recall**: `1.0000` (100.0%)
- **F1 Score**: `1.0000` (1.00)
- **ROC-AUC**: `1.0000` (1.00)

*Note: High synthetic metrics reflect tight deterministic clustering in demo scenarios. Evaluation must be updated when fine-tuned on real-world datasets.*

---

## 4. Score Decomposition & Weighting

Composite Risk Score (0–100) is transparently decomposed into three independent layers:
1. **Rule Engine Score (0–40 Points)**: 10 explainable behavioral rules.
2. **Supervised ML Score (0–35 Points)**: `RandomForestClassifier` risk probability.
3. **Graph & Anomaly Score (0–25 Points)**: `IsolationForest` decision function.

---

## 5. Graceful Fallback Mode

If model artifacts are missing or unreadable, ChainSentinel automatically falls back to **Rule-Only Mode** and displays:
> `"ML model unavailable; rule-based analysis used."`

System operation remains uninterrupted.

---

## 6. Responsible AI & Ethical Guardrails

- All UI text enforces non-definitive language: *"potentially suspicious"*, *"behavioral risk indicator"*, *"requires human review"*.
- Every report includes a visible disclaimer banner stating that scores are prioritization signals and not legal proof.
