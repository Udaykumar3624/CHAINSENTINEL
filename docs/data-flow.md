# 🔄 ChainSentinel End-to-End Data Flow Architecture (SIH26146)

This document details the central data processing pipeline of ChainSentinel, showing how user-provided data flows through validation, feature extraction, multi-engine risk scoring, graph construction, and dynamic dashboard aggregation.

---

## 📈 Central Processing Pipeline Diagram

```
[ User Input ]
   ├── Option 1: CSV Upload (POST /api/v1/dataset/upload)
   ├── Option 2: Synthetic Generator (POST /api/v1/dataset/generate)
   └── Option 3: Demo Dataset (POST /api/v1/dashboard/load-demo)
        │
        ▼
[ Preprocessing & Validation ] ──► (Invalid CSV? Return Validation Report & Error Code)
        │
        ▼
[ Active Dataset Session Store ] (app.services.dataset.store.ActiveDatasetStore)
        │
        ├──► [ Feature Extraction ] (in_degree, out_degree, PageRank, time_delta, peel_steps)
        │
        ├──► [ Rule Engine (0–40 pts) ] (Evaluates 10 behavioral heuristics)
        │
        ├──► [ ML Engine (0–35 pts) ] (RandomForest probability + IsolationForest anomaly)
        │
        ├──► [ NetworkX Graph Engine (0–25 pts) ] (Topology centrality & cycle detection)
        │
        └──► [ Composite Risk Aggregation ] (Composite Score 0–100 & Evidence Attribution)
                 │
                 ▼
[ Triage Alerts & Cases Engine ] (Generates ALT-2026 queue for high-risk entities)
                 │
                 ▼
[ Executive Dashboard API ] (GET /api/v1/dashboard/summary)
   ├── Dynamic Transactions Analyzed (actual row count)
   ├── Dynamic High/Critical Alert Count (calculated from scores ≥ 70)
   ├── Dynamic Risk Distribution (Low 0-29, Med 30-69, High 70-89, Crit 90-100)
   ├── Dynamic Risk Volume Trend (Grouped by actual timestamps)
   └── Active Dataset Provenance Banner (DATA SOURCE: Synthetic / Uploaded / Demo)
```

---

## ⚙️ Data Flow & State Management

1. **State Centralization**:  
   The `ActiveDatasetStore` singleton in `backend/app/services/dataset/store.py` holds the active dataset session in memory across backend API endpoints.

2. **Dynamic Dashboard Consumption**:  
   `GET /api/v1/dashboard/summary` reads directly from `ActiveDatasetStore`:
   - If an active dataset is set (e.g. 5,000 rows), the dashboard displays 5,000 transactions analyzed.
   - If reset (`POST /api/v1/dashboard/reset`), the dashboard displays `0` transactions analyzed with empty charts.
   - If loading demo dataset, the dashboard displays deterministic seed 42 metrics.

3. **Responsible AI Guardrail**:  
   All pipeline metrics clearly display data source provenance badges (`DATA SOURCE: SYNTHETIC DATASET` or `UPLOADED CSV`) and non-definitive risk prioritization disclaimers.
