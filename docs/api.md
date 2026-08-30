# ChainSentinel REST API Documentation

Base URL: `http://localhost:8000/api/v1`

---

## Endpoints Summary

### 1. System & Health
- `GET /health` / `GET /api/v1/health`: System health status and component checks.

### 2. Dashboard & Summary
- `GET /api/v1/dashboard/summary`: Dashboard KPIs, alert status distribution, risk breakdown, and recent alerts.

### 3. Demo Scenarios
- `GET /api/v1/demo/scenarios`: Curated SIH26146 judging scenarios (Ransomware Peeling Chain, Exchange Hot Wallet, Structuring Smurfing).

### 4. Explainable Risk Analysis
- `POST /api/v1/analyze/address`: Analyze Bitcoin address. Body: `{"address": "bc1q9..."}`.
- `POST /api/v1/analyze/transaction`: Analyze TxID. Body: `{"txid": "e3b0c..."}`.
- `POST /api/v1/analyze/csv`: Upload CSV batch file (`multipart/form-data`).

### 5. Live Blockchain Integration (Optional)
- `GET /api/v1/analyze/live/address/{address}`: Live Mempool.space address metadata.
- `GET /api/v1/analyze/live/tx/{txid}`: Live Mempool.space transaction details.
- `GET /api/v1/analyze/live/address/{address}/txs`: Live address transaction history.

### 6. Graph Intelligence
- `GET /api/v1/graph/{subject_type}/{subject_id}?hops=1|2`: Directed Cytoscape.js network topology.

### 7. Alert Management
- `GET /api/v1/alerts`: List alerts with optional status filter (`new`, `under_review`, `resolved`, `false_positive`).
- `PATCH /api/v1/alerts/{alert_id}`: Update alert status. Body: `{"status": "resolved"}`.

### 8. Case Workflow & PDF Export
- `GET /api/v1/cases`: List active cases.
- `POST /api/v1/cases`: Create case.
- `POST /api/v1/cases/{case_id}/notes`: Add analyst note.
- `GET /api/v1/cases/{case_id}/report.pdf`: Download court-ready PDF report binary.
