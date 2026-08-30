# 3-Minute SIH 2026 Judge Presentation Script

**Project Title**: ChainSentinel — AI-Powered Monitoring & Analysis of Bitcoin Transaction Traffic  
**Problem Statement**: SIH26146  

---

## ⏱️ Timeline & Walkthrough Steps

### Minute 0:00 – 0:45 | Introduction & Executive Dashboard
- **Presenter**: *"Respected Judges, Bitcoin transaction traffic is increasingly abused for ransomware laundering using complex obfuscation techniques like peeling chains, fan-out splits, and circular flows. ChainSentinel is an explainable, read-only AI investigation platform designed for law enforcement analysts."*
- **Action**: Show **Executive Dashboard** (`/`). Point out:
  1. Live KPI metrics (Total Addresses Analyzed, High-Risk Alerts, Active Cases).
  2. Risk Level Distribution Chart (Critical, High, Medium, Low).
  3. Interactive Demo Judging Scenario cards.

---

### Minute 0:45 – 1:30 | Explainable Risk Analysis & Demo Scenario
- **Presenter**: *"Let's select the judging scenario **'Ransomware Cashout & Peeling Chain'**. Notice how ChainSentinel decomposes the overall risk score into three transparent components: Rule Engine (0–40), ML Anomaly Model (0–35), and Graph Topology (0–25)."*
- **Action**: Click on Scenario 1 -> Navigate to **Risk Analysis Terminal** (`/analyze`).
- **Key Highlight**: Point to the **Structured Evidence Grid**:
  - `RULE_PEELING_CHAIN` (+10 pts): Observed 4 sequential change outputs.
  - `RULE_RAPID_FORWARDING` (+12 pts): Funds moved within 180 seconds.
  - `RULE_RISKY_NEIGHBOR` (+10 pts): Direct 1-hop distance to known flagged cluster.
- **Responsible AI Disclaimer**: Note the prominent red warning stating *"Risk scores are prioritization metrics, not legal proof of guilt."*

---

### Minute 1:30 – 2:15 | Graph Intelligence & Visual Investigation
- **Presenter**: *"Static table analysis is insufficient for tracing complex fund flows. Clicking **'Launch Graph Investigation'** opens our interactive Cytoscape.js directed graph visualizer."*
- **Action**: Navigate to **Investigation Terminal** (`/investigate/bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0`).
- **Showcase**:
  1. Color-coded nodes (Red = High/Critical Risk, Amber = Medium, Green = Low).
  2. Toggle **1-Hop vs 2-Hop Network Expansion**.
  3. Click a node to reveal its **PageRank score**, **In/Out degree**, and **Directed Cycle Detection status**.

---

### Minute 2:15 – 3:00 | Case Management & Court-Ready PDF Export
- **Presenter**: *"When high-risk behavior is confirmed, analysts can escalate the findings into an official case with notes and audit trail history, and generate a court-ready PDF report with a single click."*
- **Action**:
  1. Click **"Cases"** (`/cases`) -> Select Case `#CASE-2026-001` (*"Ransomware Cluster Campaign"*).
  2. Demonstrate adding an analyst note: *"Verified multi-hop peeling chain to mixer address."*
  3. Click **"Export Court-Ready PDF Report"**.
- **Conclusion**: *"The generated PDF includes full case metadata, behavioral signals table, audit log, and legal disclaimers. ChainSentinel provides complete end-to-end explainability for SIH26146. Thank you!"*

---

## 🏆 SIH Judge View Demo Mode (`/judge-demo`)

For live evaluator judging, navigate to **`Judge Demo`** (`/judge-demo`) in the top navigation bar.

The **Judge View** header prominently displays:
- **DATA SOURCE**: `Synthetic Dataset (Seed 42)`
- **MODE**: `Offline / Deterministic`
- **PURPOSE**: `SIH26146 Prototype Validation & Demonstration`

### 10-Step Guided Evaluator Walkthrough:
1. **STEP 1 — Load Synthetic Dataset**: Generates reproducible seed 42 dataset (100 records).
2. **STEP 2 — Show Dataset Statistics**: Displays live total transactions, unique addresses, volume BTC, and scenario breakdown.
3. **STEP 3 — Select Suspicious Entity**: Choose target entity (`bc1q9x087v...`).
4. **STEP 4 — Show Extracted Features**: Renders 11-feature vector matrix.
5. **STEP 5 — Run Risk Engines**: Executes Rule (0-40), ML (0-35), and Graph (0-25) engines.
6. **STEP 6 — Explainable Risk Score**: Composite score gauge 84/100 (HIGH) with evidence attribution.
7. **STEP 7 — Show Transaction Graph**: Interactive Cytoscape.js canvas with hop expansion.
8. **STEP 8 — Generate Alert**: Creates high-priority triage alert.
9. **STEP 9 — Create Case**: Opens official investigation case with audit log.
10. **STEP 10 — Export PDF Report**: One-click download of court-ready PDF report.

