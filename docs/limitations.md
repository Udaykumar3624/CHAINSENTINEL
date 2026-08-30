# System Limitations & Technical Scope

## 1. Technical & Operational Boundaries
- **Read-Only System**: ChainSentinel is strictly a read-only monitoring and investigation platform. It cannot execute transactions, manage wallet keys, or modify blockchain states.
- **Graph Capping (`MAX_GRAPH_NODES = 150`)**: On-demand directed graph expansion is capped at 150 nodes to maintain real-time sub-second UI rendering and prevent server memory exhaustion.
- **Demo Data Scope**: By default, ChainSentinel operates on realistic deterministic demo scenarios designed for SIH26146 judging. Live Mempool.space API integration is available via `LIVE_DATA_ENABLED=true`.

---

## 2. Machine Learning Scope & Fallback
- **Synthetic Training Corpus**: Baseline models (`RandomForestClassifier` and `IsolationForest`) are trained on synthetic transaction contexts modeled after SIH26146 judging scenarios.
- **Fallback Mode**: If model artifacts (`risk_model.joblib`) are unavailable, ChainSentinel automatically falls back to Rule-Engine-Only mode without disrupting user workflows.

---

## 3. Responsible AI & Legal Disclaimers
- **Prioritization Signals**: Risk scores (0–100) are behavioral prioritization indicators for human analysts, NOT legal proof of criminal activity.
- **No Identity Attribution**: ChainSentinel does NOT claim to identify physical individuals or prove ownership of pseudonymous Bitcoin addresses.
