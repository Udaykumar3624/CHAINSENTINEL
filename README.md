# 🛡️ ChainSentinel — AI-Powered Bitcoin Transaction Risk Analytics
> **Smart India Hackathon 2026 • Problem Statement SIH26146**  
> *Explainable, Multi-Engine Bitcoin Transaction Monitoring & Investigation Triage Platform*

---

## 📌 Executive Summary & Problem Context
Bitcoin transaction traffic presents critical forensic and regulatory challenges due to rapid multi-hop routing, pseudonymous wallet clusters, and sophisticated obfuscation topologies (peeling chains, fan-out distribution, cyclic mixing, and micro-structuring).

**ChainSentinel** is a production-grade, explainable, read-only Bitcoin transaction risk-analysis and intelligence platform engineered specifically for law enforcement and AML analysts. It combines **10 deterministic rule heuristics**, **machine learning anomaly baselines (RandomForest + IsolationForest)**, **NetworkX graph centrality analytics**, **Cytoscape.js interactive visualization**, and **ReportLab court-ready PDF dossier generation**.

---

## 🏗️ System Architecture & End-to-End Pipeline

```
Transaction Dataset (CSV / JSON / TXT / Synthetic Demo)
               │
               ▼
   [ Universal Dataset Normalizer & Validator ]
               │
               ├── Cryptographic Sanitization & Duplicate Filter
               ├── Schema Aliasing (txid, input/output, amounts, timestamps)
               ▼
   [ Multi-Engine Risk Analysis Pipeline ]
               │
   ┌───────────┼───────────────────────┐
   ▼           ▼                       ▼
Rule Engine   ML Anomaly Model        Graph Centrality
(0–40 pts)    (0–35 pts)              (0–25 pts)
10 Heuristics RandomForest + IF       NetworkX + PageRank
   │           │                       │
   └───────────┼───────────────────────┘
               ▼
   [ Composite Risk Score (0–100) ]
   (Low 0–29 | Medium 30–69 | High 70–89 | Critical 90–100)
               │
               ▼
   [ Investigation & Triage Workspace ]
   ├── Executive Dashboard (Active Dataset KPIs & Distribution)
   ├── Cytoscape.js Directed Graph Canvas (Hop Filtering & Cluster Proximity)
   ├── Triage Alert Queue & Case Management
   └── Court-Ready PDF Dossier Export (ReportLab)
```

---

## 🚀 Key Features

### 1. ⚙️ Behavioral Rule Engine (0–40 Points)
Detects 10 core adversarial transaction behaviors:
- **Rapid Forwarding**: Fast successive hops (time delta $< 10$ mins).
- **Fan-Out Splitting**: Single source splitting into multiple destination outputs.
- **Fan-In Consolidation**: Multiple source inputs aggregating into a single sink.
- **Peeling Chains**: Sequential hops peeling off change amounts.
- **Circular Flows / Cycles**: Value routed in directed loops back to origin clusters.
- **Dormancy Bursts**: Addresses dormant for $> 180$ days suddenly transmitting funds.
- **Structuring (Smurfing)**: High frequency of small-value transactions below reporting thresholds.
- **Risky-Neighbor Exposure**: Proximity to identified high-risk nodes.
- **Amount Anomaly**: Volumetric outlier deviations ($> 3\sigma$).
- **High Velocity**: High volume throughput ($> 50$ BTC in 24h).

### 2. 🧠 Machine Learning & Anomaly Baselines (0–35 Points)
- **Supervised Classifier (`RandomForest`)**: Multi-feature risk probability scoring ($0\text{--}20$ pts).
- **Unsupervised Anomaly Model (`IsolationForest`)**: Outlier volumetric spike detection ($0\text{--}15$ pts).
- **Graceful Fallback Mode**: If model artifacts are unavailable, rule heuristics maintain complete operational coverage without system interruptions.

### 3. 🕸️ Graph Intelligence & Cytoscape Terminal (0–25 Points)
- **NetworkX Topology**: On-demand directed graph analysis computing in-degree, out-degree, PageRank centrality, and shortest path distances.
- **Interactive Visualizer**: Cytoscape.js canvas with risk-tiered color coding, node inspection drawers, and browser performance safeguards (sub-graph node limits).

### 4. 📁 Universal Dataset Ingestion (CSV / JSON / TXT)
- Real-time ingestion supporting CSV, JSON arrays, and space/tab delimited TXT logs.
- Automatic column aliasing (`from_address` $\rightarrow$ `input_address`, `txid` $\rightarrow$ `transaction_id`, etc.).
- Active Dataset persistence updating dashboard metrics dynamically.

### 5. 📑 Case Management & Court-Ready PDF Dossiers
- Alert prioritization queue (`new`, `under_review`, `resolved`, `false_positive`).
- Case dossier tracking with immutable note audit trails.
- ReportLab PDF generator rendering case summaries, behavioral evidence logs, and forensic audit timestamps.

### 6. ⚖️ Responsible AI Guardrails
- **Read-Only**: Never requests, stores, or transmits private keys or seed phrases.
- **Zero Fund Interaction**: No transaction broadcasting or wallet-draining functionality.
- **Prioritization Signals**: Explicitly declared as non-definitive intelligence triage indicators requiring human investigator verification.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Cytoscape.js, Recharts, TanStack Query, Axios, Lucide Icons |
| **Backend** | Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy, NetworkX, scikit-learn, ReportLab, SlowAPI, PyJWT, Bcrypt |
| **Database** | PostgreSQL / SQLite (Automatic fast fallback) |
| **DevOps** | Docker, Docker Compose, Vercel, Render |

---

## 📂 Project Structure

```
CHAINSENTINEL/
├── .github/                 # GitHub workflows & CI configuration
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/             # API v1 routes & dependencies
│   │   ├── core/            # Config, security, logging
│   │   ├── db/              # SQLAlchemy models & sessions
│   │   ├── ml/              # RandomForest & IsolationForest pipelines
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── seed/            # Startup seeding logic
│   │   ├── services/        # Rule engine, graph analytics, PDF exporter
│   │   └── tests/           # 68+ pytest automated unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # React + TypeScript Vite frontend
│   ├── src/
│   │   ├── components/      # UI components & Cytoscape graphs
│   │   ├── context/         # AuthContext state management
│   │   ├── pages/           # Landing, Login, Dashboard, Analyze, etc.
│   │   └── services/        # API client & TypeScript interfaces
│   ├── Dockerfile
│   ├── package.json
│   └── vercel.json
├── docs/                    # Architecture, deployment, dataset specifications
│   ├── authentication.md
│   ├── data-flow.md
│   ├── dataset.md
│   ├── deployment.md
│   └── examples/            # Sample synthetic CSV, JSON, TXT datasets
├── .env.example             # Template for environment variables
├── .gitignore               # Comprehensive exclusion rules
├── docker-compose.yml       # Multi-container local deployment
├── render.yaml              # Render blueprint for FastAPI service
└── README.md
```

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.12+
- Node.js 18+ / 20+

### 1. Start Backend FastAPI Server (`http://localhost:8000`)
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### 2. Start Frontend Vite Server (`http://localhost:5173`)
```powershell
cd frontend
npm install
npm run dev
```

### 3. Run Backend Test Suite (68 Tests)
```powershell
cd backend
pytest -v app/tests/
```

---

## 🚀 Production Deployment

### Frontend (Vercel):
1. Import repository to Vercel.
2. Set Root Directory to `frontend`.
3. Set Environment Variable: `VITE_API_BASE_URL=https://your-render-backend.onrender.com/api/v1`.
4. Deploy.

### Backend (Render):
1. Create a Web Service on Render pointing to `backend` directory.
2. Build Command: `pip install -r requirements.txt`.
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Configure environment variables (`JWT_SECRET_KEY`, `CORS_ORIGINS`, `DATABASE_URL`).

---

## 🔒 Security & Privacy Notice
ChainSentinel does not collect or log plaintext passwords, private keys, or wallet credentials. All analyzed blockchain transactions and synthetic datasets are processed strictly as read-only cryptographic telemetry.

---

## 📜 License
Smart India Hackathon 2026 • Problem Statement SIH26146
