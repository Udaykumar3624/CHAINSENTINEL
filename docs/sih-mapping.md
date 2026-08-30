# Problem Statement SIH26146 Requirement Mapping

## Problem Statement Title
> **"AI-Powered Monitoring & Analysis of Bitcoin Transaction Traffic"**

| SIH26146 Requirement / Objective | ChainSentinel Implementation & Code Location | Status |
| :--- | :--- | :--- |
| **Explainable Bitcoin Transaction Risk Analysis** | `backend/app/services/analysis/analysis_service.py`<br>`backend/app/services/analysis/rule_engine.py`<br>Evaluates 10 distinct rule heuristics returning structured `SignalItem` objects with code, score, explanation, observed values, and recommended review steps. | **COMPLETED** |
| **Graph Topology & Anomaly Detection** | `backend/app/services/graph/graph_service.py`<br>`frontend/src/components/CytoscapeGraph.tsx`<br>Directed NetworkX graph analysis computing PageRank, degree centrality, cycle detection, shortest path to flagged clusters, and Cytoscape.js canvas visualization. | **COMPLETED** |
| **Machine Learning Baseline & Anomaly Scoring** | `backend/app/ml/feature_engineering.py`<br>`backend/app/ml/train.py`<br>`backend/app/ml/inference.py`<br>Combines `RandomForestClassifier` (0–35 pts) and `IsolationForest` (0–25 pts) with joblib artifact persistence and graceful fallback mode. | **COMPLETED** |
| **Read-Only Operation & Safety** | `backend/app/core/security.py`<br>Read-only design with zero private key handling, zero transaction broadcast capabilities, and mandatory Responsible AI disclaimers. | **COMPLETED** |
| **Alert Management & Case Workflow** | `backend/app/api/routes/alerts.py`<br>`backend/app/api/routes/cases.py`<br>`frontend/src/pages/AlertsPage.tsx`<br>`frontend/src/pages/CasesPage.tsx`<br>Full alert queue triage, case management with analyst notes timeline, status transitions, and audit logs. | **COMPLETED** |
| **Court-Ready Case PDF Export** | `backend/app/services/reports/pdf_generator.py`<br>Generates ReportLab binary PDF reports with case metadata, behavioral evidence table, linked entities, notes timeline, and legal disclaimers. | **COMPLETED** |
| **Live Blockchain Lookup with Fallback** | `backend/app/services/providers/mempool_provider.py`<br>`backend/app/services/providers/demo_provider.py`<br>Optional Mempool.space API integration with input regex validation, rate limiting, and fallback to Demo Mode. | **COMPLETED** |
