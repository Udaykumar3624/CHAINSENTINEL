import React from 'react';
import { Link } from 'react-router-dom';
import {
  Shield,
  Activity,
  Search,
  Cpu,
  Network,
  Lock,
  ArrowRight,
  Database,
  CheckCircle2,
  AlertTriangle,
  FileText,
  Layers,
  BarChart3,
  Scale,
  Eye,
  GitBranch,
  UploadCloud,
  FileCode,
  FileSpreadsheet,
  Workflow,
  Sparkles,
  ChevronRight,
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Background Subtle Cyber Grid & Ambient Glow */}
      <div className="fixed inset-0 bg-[linear-gradient(to_right,#131d35_1px,transparent_1px),linear-gradient(to_bottom,#131d35_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_75%_50%_at_50%_0%,#000_70%,transparent_100%)] opacity-25 pointer-events-none" />
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[350px] bg-gradient-to-b from-cyan-500/10 via-blue-500/5 to-transparent blur-3xl pointer-events-none rounded-full" />

      {/* ==================================================
          1. PUBLIC HEADER & NAVIGATION
         ================================================== */}
      <header className="sticky top-0 z-50 bg-[#070b14]/90 backdrop-blur-md border-b border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Brand Logo & Title */}
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400 shadow-lg shadow-cyan-950/40">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-bold text-base tracking-wider text-slate-100 uppercase font-mono">
                    CHAIN<span className="text-cyan-400">SENTINEL</span>
                  </span>
                  <span className="px-2 py-0.5 text-[10px] font-mono tracking-wide uppercase bg-slate-800 border border-slate-700 text-cyan-400 rounded">
                    SIH26146
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 font-mono hidden sm:block">
                  Bitcoin AI Risk Analytics
                </p>
              </div>
            </div>

            {/* Navigation Anchor Links */}
            <nav className="hidden lg:flex items-center space-x-6 text-xs font-medium text-slate-300">
              <a href="#overview" className="hover:text-cyan-400 transition-colors">Overview</a>
              <a href="#how-it-works" className="hover:text-cyan-400 transition-colors">How It Works</a>
              <a href="#features" className="hover:text-cyan-400 transition-colors">Features</a>
              <a href="#risk-scoring" className="hover:text-cyan-400 transition-colors">Risk Scoring</a>
              <a href="#datasets" className="hover:text-cyan-400 transition-colors">Datasets</a>
              <a href="#responsible-ai" className="hover:text-cyan-400 transition-colors">Responsible AI</a>
            </nav>

            {/* Investigator Login CTA */}
            <div className="flex items-center space-x-3">
              <Link
                to="/login"
                className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-xs rounded-lg transition-all shadow-lg shadow-cyan-950/50 flex items-center space-x-1.5 group"
              >
                <span>Investigator Login</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* ==================================================
          2. HERO SECTION
         ================================================== */}
      <section className="relative pt-16 pb-20 md:pt-24 md:pb-28 overflow-hidden">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6 relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 font-mono text-xs font-semibold tracking-wide uppercase">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Smart India Hackathon 2026 • Problem Statement SIH26146</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-slate-100 font-mono">
            Chain<span className="text-cyan-400">Sentinel</span>
          </h1>

          <p className="text-lg sm:text-xl md:text-2xl text-cyan-300/90 font-medium max-w-3xl mx-auto">
            Explainable Bitcoin Risk Analytics for Transaction Intelligence
          </p>

          <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto leading-relaxed">
            An explainable, read-only platform that analyzes Bitcoin transaction
            behavior, graph relationships, and statistical anomalies to prioritize
            potentially suspicious activity for human investigation.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link
              to="/login"
              className="w-full sm:w-auto px-6 py-3.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-sm rounded-xl transition-all shadow-xl shadow-cyan-950/60 flex items-center justify-center space-x-2 group"
            >
              <span>Investigator Login</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>

            <a
              href="#how-it-works"
              className="w-full sm:w-auto px-6 py-3.5 bg-slate-900/80 hover:bg-slate-800 text-slate-200 border border-slate-800 font-bold text-sm rounded-xl transition-all flex items-center justify-center space-x-2"
            >
              <Workflow className="w-4 h-4 text-cyan-400" />
              <span>Explore How It Works</span>
            </a>
          </div>

          {/* Quick Metrics Bar */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 max-w-4xl mx-auto pt-10 font-mono">
            <div className="p-3.5 bg-slate-900/50 border border-slate-800/80 rounded-xl text-left">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Rule Engine</span>
              <span className="text-base font-bold text-cyan-400">10 Heuristics</span>
            </div>
            <div className="p-3.5 bg-slate-900/50 border border-slate-800/80 rounded-xl text-left">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">ML Baseline</span>
              <span className="text-base font-bold text-purple-400">RandomForest + IF</span>
            </div>
            <div className="p-3.5 bg-slate-900/50 border border-slate-800/80 rounded-xl text-left">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Graph Engine</span>
              <span className="text-base font-bold text-amber-400">NetworkX + PageRank</span>
            </div>
            <div className="p-3.5 bg-slate-900/50 border border-slate-800/80 rounded-xl text-left">
              <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Audit Output</span>
              <span className="text-base font-bold text-emerald-400">Court-Ready PDF</span>
            </div>
          </div>
        </div>
      </section>

      {/* ==================================================
          3. PROJECT OVERVIEW
         ================================================== */}
      <section id="overview" className="py-16 bg-slate-900/40 border-y border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
          <div className="text-center space-y-2 max-w-3xl mx-auto">
            <h2 className="text-xs font-mono text-cyan-400 uppercase tracking-widest font-bold">
              Project Overview
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100 font-mono">
              WHAT IS CHAINSENTINEL?
            </h3>
            <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
              ChainSentinel analyzes Bitcoin transaction data using multiple complementary analysis layers:
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-2.5">
              <div className="p-2.5 bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 rounded-lg w-fit">
                <Cpu className="w-5 h-5" />
              </div>
              <h4 className="text-xs font-bold text-slate-200 uppercase font-mono">Rule-Based Heuristics</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Deterministic detection of rapid forwarding, peeling chains, fan-out/in, structuring, and loops.
              </p>
            </div>

            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-2.5">
              <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 text-purple-400 rounded-lg w-fit">
                <Activity className="w-5 h-5" />
              </div>
              <h4 className="text-xs font-bold text-slate-200 uppercase font-mono">ML Anomaly Detection</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                RandomForest supervised classification and IsolationForest unsupervised volumetric outlier scoring.
              </p>
            </div>

            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-2.5">
              <div className="p-2.5 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-lg w-fit">
                <Network className="w-5 h-5" />
              </div>
              <h4 className="text-xs font-bold text-slate-200 uppercase font-mono">Graph Analytics</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Topological analysis with NetworkX calculating in/out degrees, PageRank, and cluster distances.
              </p>
            </div>

            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-2.5">
              <div className="p-2.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-lg w-fit">
                <BarChart3 className="w-5 h-5" />
              </div>
              <h4 className="text-xs font-bold text-slate-200 uppercase font-mono">Risk Scoring</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Transparent 0–100 risk prioritization score with comprehensive factor contribution breakdowns.
              </p>
            </div>

            <div className="p-5 bg-slate-950/70 border border-slate-800 rounded-xl space-y-2.5">
              <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg w-fit">
                <FileText className="w-5 h-5" />
              </div>
              <h4 className="text-xs font-bold text-slate-200 uppercase font-mono">Investigation Support</h4>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Alert queues, investigation cases, immutable audit notes, and court-ready PDF dossier exports.
              </p>
            </div>
          </div>

          {/* Primary Legal & Ethical Guardrail Callout */}
          <div className="p-4 bg-cyan-950/30 border border-cyan-500/30 rounded-xl flex items-start space-x-3 text-cyan-200 text-xs leading-relaxed max-w-4xl mx-auto">
            <Scale className="w-5 h-5 text-cyan-400 shrink-0 mt-0.5" />
            <p>
              <strong className="font-semibold text-cyan-300">Responsible AI Notice:</strong> ChainSentinel provides risk prioritization signals for investigative triage. It does not determine criminal guilt or identify individuals.
            </p>
          </div>
        </div>
      </section>

      {/* ==================================================
          4. HOW IT WORKS WORKFLOW PIPELINE
         ================================================== */}
      <section id="how-it-works" className="py-16 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          <div className="text-center space-y-2 max-w-3xl mx-auto">
            <h2 className="text-xs font-mono text-cyan-400 uppercase tracking-widest font-bold">
              Investigation Pipeline
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100 font-mono">
              HOW IT WORKS
            </h3>
            <p className="text-xs sm:text-sm text-slate-400">
              End-to-end data processing from ingestion to human analyst review.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
            {/* Step 1 */}
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-cyan-500/10 text-cyan-400 rounded text-[10px] font-bold">STEP 01</span>
              <div className="flex items-center space-x-2 text-slate-200 font-bold">
                <Database className="w-4 h-4 text-cyan-400" />
                <span>Transaction Dataset</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                Ingest transactions via CSV, JSON, TXT, or deterministic synthetic demo generators.
              </p>
            </div>

            {/* Step 2 */}
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-cyan-500/10 text-cyan-400 rounded text-[10px] font-bold">STEP 02</span>
              <div className="flex items-center space-x-2 text-slate-200 font-bold">
                <Layers className="w-4 h-4 text-cyan-400" />
                <span>Data Normalization</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                Schema verification, duplicate filtering, column aliasing, and cryptographic sanitization.
              </p>
            </div>

            {/* Step 3 */}
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-cyan-500/10 text-cyan-400 rounded text-[10px] font-bold">STEP 03</span>
              <div className="flex items-center space-x-2 text-slate-200 font-bold">
                <Cpu className="w-4 h-4 text-cyan-400" />
                <span>Behavioral Rule Engine</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                Evaluate 10 transparent rule heuristics (0–40 pts) detecting obfuscation topologies.
              </p>
            </div>

            {/* Step 4 */}
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-purple-500/10 text-purple-400 rounded text-[10px] font-bold">STEP 04</span>
              <div className="flex items-center space-x-2 text-slate-200 font-bold">
                <Activity className="w-4 h-4 text-purple-400" />
                <span>ML Anomaly Analysis</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                Supervised risk classification + unsupervised statistical outlier scoring (0–35 pts).
              </p>
            </div>

            {/* Step 5 */}
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-amber-500/10 text-amber-400 rounded text-[10px] font-bold">STEP 05</span>
              <div className="flex items-center space-x-2 text-slate-200 font-bold">
                <Network className="w-4 h-4 text-amber-400" />
                <span>Graph Analysis</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                NetworkX graph topology, PageRank centrality, and cluster proximity metrics (0–25 pts).
              </p>
            </div>

            {/* Step 6 */}
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-rose-500/10 text-rose-400 rounded text-[10px] font-bold">STEP 06</span>
              <div className="flex items-center space-x-2 text-slate-200 font-bold">
                <BarChart3 className="w-4 h-4 text-rose-400" />
                <span>Composite Risk Score</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                Bounded 0–100 composite score categorized into Low, Medium, High, or Critical risk.
              </p>
            </div>

            {/* Step 7 */}
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 rounded text-[10px] font-bold">STEP 07</span>
              <div className="flex items-center space-x-2 text-slate-200 font-bold">
                <AlertTriangle className="w-4 h-4 text-emerald-400" />
                <span>Alerts & Investigation</span>
              </div>
              <p className="text-[11px] text-slate-400 font-sans">
                Automatic alert triage generation, case tracking, note logging, and Cytoscape visualization.
              </p>
            </div>

            {/* Step 8 */}
            <div className="p-4 bg-slate-900/60 border border-cyan-500/40 bg-cyan-950/20 rounded-xl space-y-2 relative">
              <span className="px-2 py-0.5 bg-cyan-500/20 text-cyan-300 rounded text-[10px] font-bold">STEP 08</span>
              <div className="flex items-center space-x-2 text-cyan-300 font-bold">
                <Eye className="w-4 h-4 text-cyan-400" />
                <span>Human Analyst Review</span>
              </div>
              <p className="text-[11px] text-slate-300 font-sans">
                Investigator validates signals, examines evidence trails, and exports court-ready PDF reports.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ==================================================
          5. CORE FEATURES
         ================================================== */}
      <section id="features" className="py-16 bg-slate-900/40 border-y border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          <div className="text-center space-y-2 max-w-3xl mx-auto">
            <h2 className="text-xs font-mono text-cyan-400 uppercase tracking-widest font-bold">
              Platform Capabilities
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100 font-mono">
              CORE FEATURES
            </h3>
            <p className="text-xs sm:text-sm text-slate-400">
              A comprehensive toolset engineered for financial intelligence and anti-money laundering triage.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <div className="p-6 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3">
              <div className="p-3 bg-cyan-500/10 text-cyan-400 rounded-xl w-fit">
                <UploadCloud className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 font-mono">1. Dataset Analysis</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Upload and analyze supported transaction datasets (CSV, JSON, TXT) with real-time validation and zero hardcoding.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="p-6 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3">
              <div className="p-3 bg-rose-500/10 text-rose-400 rounded-xl w-fit">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 font-mono">2. Behavioral Risk Detection</h4>
              <p className="text-xs text-slate-400 leading-relaxed mb-2">
                Detect 8 core adversarial money-laundering patterns:
              </p>
              <ul className="text-[11px] text-slate-400 space-y-1 font-mono">
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Rapid forwarding (&lt;10 min hop)</span></li>
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Fan-out distribution splitting</span></li>
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Fan-in wallet consolidation</span></li>
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Peeling chains (change peel hops)</span></li>
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Circular flows & mixing loops</span></li>
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Dormancy bursts (&gt;180 days reactivated)</span></li>
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Structuring / Micro-tx smurfing</span></li>
                <li className="flex items-center space-x-1.5"><ChevronRight className="w-3 h-3 text-cyan-400" /><span>Risky-neighbor cluster exposure</span></li>
              </ul>
            </div>

            {/* Feature 3 */}
            <div className="p-6 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3">
              <div className="p-3 bg-purple-500/10 text-purple-400 rounded-xl w-fit">
                <Cpu className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 font-mono">3. ML Analysis</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Use anomaly and risk models (RandomForest and IsolationForest) to identify non-linear unusual transaction behavior.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="p-6 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3">
              <div className="p-3 bg-amber-500/10 text-amber-400 rounded-xl w-fit">
                <Network className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 font-mono">4. Graph Intelligence</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Analyze multi-hop transaction relationships using NetworkX graph topology and interactive Cytoscape.js canvas rendering.
              </p>
            </div>

            {/* Feature 5 */}
            <div className="p-6 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3">
              <div className="p-3 bg-cyan-500/10 text-cyan-400 rounded-xl w-fit">
                <BarChart3 className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 font-mono">5. Risk Scoring</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Generate an explainable 0–100 prioritization score with transparent sub-score weights and human-readable evidence summaries.
              </p>
            </div>

            {/* Feature 6 */}
            <div className="p-6 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3">
              <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl w-fit">
                <FileText className="w-6 h-6" />
              </div>
              <h4 className="text-sm font-bold text-slate-100 font-mono">6. Investigation Workflow</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                Complete triage workflow with automated alert generation, case timelines, analyst notes, and court-ready ReportLab PDF exports.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ==================================================
          6. RISK SCORE EXPLANATION
         ================================================== */}
      <section id="risk-scoring" className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
          <div className="text-center space-y-2 max-w-3xl mx-auto">
            <h2 className="text-xs font-mono text-cyan-400 uppercase tracking-widest font-bold">
              Transparent Scoring Framework
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100 font-mono">
              RISK SCORE EXPLANATION
            </h3>
            <p className="text-xs sm:text-sm text-slate-400">
              ChainSentinel computes a multi-layered composite score between 0 and 100 for every evaluated entity.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono">
            {/* Rule Engine Weight */}
            <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-xl space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-cyan-400 uppercase">Rule Engine</span>
                <span className="text-sm font-bold text-slate-100">0–40 Points</span>
              </div>
              <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                <div className="h-full bg-cyan-400 w-[40%]" />
              </div>
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                Evaluates 10 deterministic heuristics (rapid forwarding, peeling chains, fan-out/in, structuring, dormancy burst, cycles).
              </p>
            </div>

            {/* ML Baseline Weight */}
            <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-xl space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-purple-400 uppercase">ML Baseline</span>
                <span className="text-sm font-bold text-slate-100">0–35 Points</span>
              </div>
              <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                <div className="h-full bg-purple-400 w-[35%]" />
              </div>
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                RandomForest supervised classification score (0–20 pts) + IsolationForest anomaly spike detection (0–15 pts).
              </p>
            </div>

            {/* Graph Centrality Weight */}
            <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-xl space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-amber-400 uppercase">Graph Centrality</span>
                <span className="text-sm font-bold text-slate-100">0–25 Points</span>
              </div>
              <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                <div className="h-full bg-amber-400 w-[25%]" />
              </div>
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                NetworkX graph metrics including in/out degree ratios, PageRank centrality, and shortest path to high-risk clusters.
              </p>
            </div>
          </div>

          {/* Composite Classification Levels Table */}
          <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-6 space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 font-mono">
              Composite Risk Score Classifications:
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded font-bold text-[10px]">
                  0 – 29
                </span>
                <p className="font-bold text-emerald-400 text-sm">LOW RISK</p>
                <p className="text-[11px] text-slate-400 font-sans">Normal baseline activity with negligible anomaly signals.</p>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded font-bold text-[10px]">
                  30 – 69
                </span>
                <p className="font-bold text-amber-400 text-sm">MEDIUM RISK</p>
                <p className="text-[11px] text-slate-400 font-sans">Moderate behavioral irregularities requiring periodic monitoring.</p>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-orange-500/10 text-orange-400 border border-orange-500/30 rounded font-bold text-[10px]">
                  70 – 89
                </span>
                <p className="font-bold text-orange-400 text-sm">HIGH RISK</p>
                <p className="text-[11px] text-slate-400 font-sans">Multiple severe obfuscation flags present; immediate triage recommended.</p>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                <span className="px-2 py-0.5 bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded font-bold text-[10px]">
                  90 – 100
                </span>
                <p className="font-bold text-rose-400 text-sm">CRITICAL RISK</p>
                <p className="text-[11px] text-slate-400 font-sans">Extreme multi-engine heuristic match; formal case escalation created.</p>
              </div>
            </div>
            <p className="text-[11px] text-slate-400 font-mono italic">
              * The risk score is an investigative prioritization signal, not definitive proof of criminal intent.
            </p>
          </div>
        </div>
      </section>

      {/* ==================================================
          7. DATASET & INPUT FORMATS SECTION
         ================================================== */}
      <section id="datasets" className="py-16 bg-slate-900/40 border-y border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
          <div className="text-center space-y-2 max-w-3xl mx-auto">
            <h2 className="text-xs font-mono text-cyan-400 uppercase tracking-widest font-bold">
              Data Ingestion
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100 font-mono">
              SUPPORTED TRANSACTION DATASETS
            </h3>
            <p className="text-xs sm:text-sm text-slate-400">
              Users can provide transaction data for analysis instead of relying only on the built-in demonstration dataset.
            </p>
          </div>

          {/* Formats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-cyan-500/10 text-cyan-400 rounded-lg">
                  <FileSpreadsheet className="w-5 h-5" />
                </div>
                <h4 className="font-bold font-mono text-sm text-slate-200">CSV Datasets</h4>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Standard comma-separated files containing transaction headers (`transaction_id`, `input_address`, `output_address`, `amount_btc`, `timestamp`).
              </p>
              <span className="inline-block px-2.5 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 text-[10px] font-mono rounded">
                .csv format supported
              </span>
            </div>

            <div className="p-6 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-purple-500/10 text-purple-400 rounded-lg">
                  <FileCode className="w-5 h-5" />
                </div>
                <h4 className="font-bold font-mono text-sm text-slate-200">JSON Objects & Arrays</h4>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Structured array of transaction objects or nested block records with automatic field alias normalizer.
              </p>
              <span className="inline-block px-2.5 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/30 text-[10px] font-mono rounded">
                .json format supported
              </span>
            </div>

            <div className="p-6 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
              <div className="flex items-center space-x-3">
                <div className="p-2.5 bg-amber-500/10 text-amber-400 rounded-lg">
                  <FileText className="w-5 h-5" />
                </div>
                <h4 className="font-bold font-mono text-sm text-slate-200">TXT Tab/Space Delimited</h4>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Plain-text log dumps and tab/space separated forensic ledger exports with automatic delimiter inference.
              </p>
              <span className="inline-block px-2.5 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/30 text-[10px] font-mono rounded">
                .txt format supported
              </span>
            </div>
          </div>

          {/* Demo Data Clarification Callout */}
          <div className="p-5 bg-slate-950/80 border border-slate-800 rounded-xl flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="space-y-1 text-left">
              <div className="flex items-center space-x-2">
                <span className="px-2 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/30 text-[10px] font-mono rounded font-bold uppercase">
                  DEMO / SYNTHETIC DATA
                </span>
                <h4 className="font-mono text-xs font-bold text-slate-200">Reproducible Demonstration Scenarios</h4>
              </div>
              <p className="text-xs text-slate-400">
                Built-in deterministic demo scenarios are available for SIH demonstration and reproducible testing.
              </p>
            </div>

            <Link
              to="/dataset"
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-xs rounded-lg transition-all shadow-lg shadow-cyan-950/50 flex items-center space-x-1.5 shrink-0"
            >
              <UploadCloud className="w-4 h-4" />
              <span>Upload / Analyze Dataset</span>
            </Link>
          </div>
        </div>
      </section>

      {/* ==================================================
          8. RESPONSIBLE AI & ETHICAL GUARDRAILS
         ================================================== */}
      <section id="responsible-ai" className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
          <div className="text-center space-y-2 max-w-3xl mx-auto">
            <h2 className="text-xs font-mono text-cyan-400 uppercase tracking-widest font-bold">
              Ethical AI & Compliance
            </h2>
            <h3 className="text-2xl sm:text-3xl font-bold text-slate-100 font-mono">
              RESPONSIBLE AI SAFEGUARDS
            </h3>
            <p className="text-xs sm:text-sm text-slate-400">
              ChainSentinel is strictly designed as an analytical triage assistant adhering to rigorous compliance boundaries.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <h4 className="font-bold text-slate-200 uppercase">Read-Only Analysis</h4>
              <p className="text-[11px] text-slate-400 font-sans">
                Never requests, requires, or stores private keys, seed phrases, or wallet credentials.
              </p>
            </div>

            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <h4 className="font-bold text-slate-200 uppercase">Zero Fund Interaction</h4>
              <p className="text-[11px] text-slate-400 font-sans">
                No transaction broadcasting, signing capabilities, or wallet-draining functionality.
              </p>
            </div>

            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <h4 className="font-bold text-slate-200 uppercase">Human-In-The-Loop</h4>
              <p className="text-[11px] text-slate-400 font-sans">
                All risk scores are prioritization signals intended strictly to guide human investigator review.
              </p>
            </div>

            <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl space-y-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-400" />
              <h4 className="font-bold text-slate-200 uppercase">Non-Definitive Attribution</h4>
              <p className="text-[11px] text-slate-400 font-sans">
                Makes no claim of legal guilt or individual identity; evaluates pseudonymous network traffic patterns.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ==================================================
          9. CALL TO ACTION / FOOTER
         ================================================== */}
      <footer className="bg-slate-950 border-t border-slate-800/80 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-cyan-500/10 border border-cyan-500/30 rounded-xl text-cyan-400">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <span className="font-bold text-base tracking-wider text-slate-100 uppercase font-mono">
                  ChainSentinel
                </span>
                <p className="text-xs text-slate-500 font-mono">
                  Smart India Hackathon 2026 • Problem Statement SIH26146
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono font-bold text-xs rounded-xl transition-all shadow-lg shadow-cyan-950/50 flex items-center space-x-1.5"
              >
                <span>Investigator Login →</span>
              </Link>
            </div>
          </div>

          <div className="pt-6 border-t border-slate-900 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500 font-mono gap-3">
            <p>© 2026 ChainSentinel • AI-Powered Bitcoin Transaction Monitoring Platform</p>
            <p>Confidential & Authorized Law Enforcement Triage Assistant</p>
          </div>
        </div>
      </footer>
    </div>
  );
};
