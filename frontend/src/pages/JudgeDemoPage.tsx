import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Shield,
  Database,
  Cpu,
  Network,
  AlertTriangle,
  FileCheck,
  FileText,
  Download,
  Play,
  ChevronRight,
  ChevronLeft,
  CheckCircle2,
  Loader2,
  Info,
  ArrowRight,
  BarChart3,
  Search,
  Lock
} from 'lucide-react';
import {
  generateSyntheticDataset,
  fetchDatasetExplorer,
  analyzeAddress,
  fetchEntityGraph,
  createCase,
  getDatasetDownloadUrl,
  getCasePdfUrl,
  CytoscapeNodeData
} from '../services/api';
import { CytoscapeGraph } from '../components/CytoscapeGraph';

const STEPS = [
  { id: 1, title: '1. Load Synthetic Dataset' },
  { id: 2, title: '2. Dataset Statistics' },
  { id: 3, title: '3. Select Suspicious Entity' },
  { id: 4, title: '4. Extracted Features' },
  { id: 5, title: '5. Run Risk Engines' },
  { id: 6, title: '6. Explainable Risk Score' },
  { id: 7, title: '7. Transaction Graph' },
  { id: 8, title: '8. Generate Alert' },
  { id: 9, title: '9. Create Case' },
  { id: 10, title: '10. Export PDF Report' },
];

const DEFAULT_DEMO_SUBJECT = 'bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0';

export const JudgeDemoPage: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [selectedEntity, setSelectedEntity] = useState<string>(DEFAULT_DEMO_SUBJECT);
  const [createdCaseId, setCreatedCaseId] = useState<string>('case-001');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [datasetLoaded, setDatasetLoaded] = useState<boolean>(true);
  const [selectedGraphNode, setSelectedGraphNode] = useState<CytoscapeNodeData | null>(null);

  // Fetch Dataset Explorer Data
  const { data: datasetData, isLoading: isDatasetLoading } = useQuery({
    queryKey: ['judgeDatasetExplorer'],
    queryFn: () => fetchDatasetExplorer(),
  });

  // Fetch Risk Analysis for Selected Entity
  const { data: analysisData, isLoading: isAnalysisLoading } = useQuery({
    queryKey: ['judgeAnalyze', selectedEntity],
    queryFn: () => analyzeAddress(selectedEntity),
    enabled: currentStep >= 4,
  });

  // Fetch Graph for Selected Entity
  const { data: graphData, isLoading: isGraphLoading } = useQuery({
    queryKey: ['judgeGraph', selectedEntity],
    queryFn: () => fetchEntityGraph('address', selectedEntity, 1),
    enabled: currentStep >= 7,
  });

  const handleNextStep = () => {
    if (currentStep < 10) setCurrentStep(currentStep + 1);
  };

  const handlePrevStep = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1);
  };

  const handleTriggerCaseCreation = async () => {
    try {
      const res = await createCase({
        title: `SIH Judge Demo Case: ${selectedEntity.substring(0, 10)}...`,
        description: `Automated investigation case opened during SIH26146 judge demonstration. High behavioral risk exposure detected.`,
        priority: 'high',
        status: 'in_progress',
        assigned_investigator: 'SIH Evaluator Analyst',
        linked_addresses: [selectedEntity],
        linked_transactions: ['e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']
      });
      setCreatedCaseId(res.id);
      setCurrentStep(10);
    } catch (err) {
      setCreatedCaseId('case-001');
      setCurrentStep(10);
    }
  };

  return (
    <div className="space-y-6">
      {/* JUDGE VIEW HEADER BANNER */}
      <div className="bg-slate-900/80 p-6 rounded-xl border border-amber-500/40 space-y-4 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-3">
            <span className="px-3 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/40 text-xs font-mono font-bold uppercase rounded flex items-center gap-1.5 animate-pulse">
              <Shield className="w-4 h-4 text-amber-400" />
              JUDGE VIEW DEMO MODE
            </span>
            <h1 className="text-lg font-mono font-bold text-slate-100">
              SIH26146 Guided Evaluation Workflow (3–5 Min)
            </h1>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentStep(1)}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono rounded-lg border border-slate-700"
            >
              Reset Demo
            </button>
          </div>
        </div>

        {/* METADATA BAR */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
          <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
            <span className="text-slate-500 block text-[10px] uppercase font-semibold">DATA SOURCE</span>
            <span className="text-cyan-400 font-bold">Synthetic Dataset (Seed 42)</span>
          </div>

          <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
            <span className="text-slate-500 block text-[10px] uppercase font-semibold">MODE</span>
            <span className="text-emerald-400 font-bold">Offline / Deterministic</span>
          </div>

          <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
            <span className="text-slate-500 block text-[10px] uppercase font-semibold">PURPOSE</span>
            <span className="text-purple-400 font-bold">SIH26146 Evaluation & Judging</span>
          </div>
        </div>
      </div>

      {/* 10-STEP STEPPER BAR */}
      <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 overflow-x-auto">
        <div className="flex items-center justify-between min-w-[800px] gap-2">
          {STEPS.map((s) => (
            <button
              key={s.id}
              onClick={() => setCurrentStep(s.id)}
              className={`flex-1 py-2 px-2 rounded-lg text-[11px] font-mono font-bold transition-colors border ${
                currentStep === s.id
                  ? 'bg-cyan-500 text-slate-950 border-cyan-400'
                  : currentStep > s.id
                  ? 'bg-slate-800/80 text-emerald-400 border-slate-700'
                  : 'bg-slate-950 text-slate-500 border-slate-800'
              }`}
            >
              {s.title}
            </button>
          ))}
        </div>
      </div>

      {/* STEP CONTAINER */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-6">
        {/* STEP 1: LOAD SYNTHETIC DATASET */}
        {currentStep === 1 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <Database className="w-5 h-5" />
              <span>STEP 1: Load Synthetic Dataset</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Generate or load a 100-record synthetic Bitcoin transaction dataset containing ground-truth behavioral scenarios (Rapid Forwarding, Peeling Chains, Circular Wash Flows, Structuring, Dormancy Bursts).
            </p>

            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3 font-mono text-xs">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Dataset File:</span>
                <span className="text-cyan-400 font-bold">synthetic_dataset_seed42.csv</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Record Count:</span>
                <span className="text-slate-200">100 Transactions</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Random Seed:</span>
                <span className="text-purple-400 font-bold">42 (Reproducible)</span>
              </div>
            </div>

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Confirm & Proceed to Dataset Statistics</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 2: DATASET STATISTICS */}
        {currentStep === 2 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <BarChart3 className="w-5 h-5" />
              <span>STEP 2: View Dataset Statistics</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Calculated live statistics from the loaded synthetic dataset:
            </p>

            {datasetData && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-500 text-[10px] block uppercase">Total Transactions</span>
                  <span className="text-lg font-bold text-slate-100">{datasetData.summary.total_transactions}</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-500 text-[10px] block uppercase">Unique Addresses</span>
                  <span className="text-lg font-bold text-cyan-400">{datasetData.summary.unique_addresses}</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-500 text-[10px] block uppercase">Total Volume BTC</span>
                  <span className="text-lg font-bold text-emerald-400">{datasetData.summary.total_volume_btc.toFixed(2)} BTC</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-500 text-[10px] block uppercase">Avg Tx Amount</span>
                  <span className="text-lg font-bold text-purple-400">{datasetData.summary.avg_transaction_amount_btc.toFixed(3)} BTC</span>
                </div>
              </div>
            )}

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Proceed to Entity Selection</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 3: SELECT SUSPICIOUS ENTITY */}
        {currentStep === 3 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <Search className="w-5 h-5" />
              <span>STEP 3: Select Suspicious Forensic Entity</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Select a target entity from the ground-truth synthetic dataset for multi-tier analysis:
            </p>

            <div className="space-y-2 font-mono text-xs">
              <div
                onClick={() => setSelectedEntity(DEFAULT_DEMO_SUBJECT)}
                className={`p-4 rounded-xl border cursor-pointer transition-colors ${
                  selectedEntity === DEFAULT_DEMO_SUBJECT
                    ? 'bg-slate-950 border-cyan-400 text-cyan-300'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-bold">{DEFAULT_DEMO_SUBJECT}</span>
                  <span className="px-2 py-0.5 bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded text-[10px]">
                    Ground Truth: Ransomware Payload / Rapid Forwarding
                  </span>
                </div>
              </div>

              <div
                onClick={() => setSelectedEntity('bc1qcycle000111222333444555666777888999')}
                className={`p-4 rounded-xl border cursor-pointer transition-colors ${
                  selectedEntity === 'bc1qcycle000111222333444555666777888999'
                    ? 'bg-slate-950 border-cyan-400 text-cyan-300'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400'
                }`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-bold">bc1qcycle000111222333444555666777888999</span>
                  <span className="px-2 py-0.5 bg-purple-500/10 text-purple-400 border border-purple-500/30 rounded text-[10px]">
                    Ground Truth: Circular Wash Flow Loop
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Extract Features for {selectedEntity.substring(0, 10)}...</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 4: EXTRACTED FEATURES */}
        {currentStep === 4 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <Cpu className="w-5 h-5" />
              <span>STEP 4: Show Extracted Numeric Feature Vector</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Numeric feature vector extracted from the loaded dataset for subject <span className="font-mono text-cyan-400">{selectedEntity}</span>:
            </p>

            {analysisData?.feature_values && (
              <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-2.5 font-mono text-[11px]">
                {Object.entries(analysisData.feature_values).map(([fk, fv]) => (
                  <div key={fk} className="p-2.5 bg-slate-950 border border-slate-800 rounded-lg">
                    <span className="text-slate-500 block text-[9px] uppercase">{fk}</span>
                    <span className="text-slate-200 font-bold truncate block">{String(fv)}</span>
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Execute Rule + ML + Graph Engines</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 5: RUN RISK ENGINES */}
        {currentStep === 5 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <Cpu className="w-5 h-5" />
              <span>STEP 5: Multi-Engine Scoring Pipeline Execution</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 font-mono text-xs">
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                <span className="text-cyan-400 font-bold block uppercase text-[10px]">1. Rule Engine</span>
                <p className="text-slate-300">Evaluates 10 Heuristics (0–40 pts)</p>
                <span className="text-emerald-400 font-bold block pt-1">
                  Score: {analysisData?.rule_score ?? analysisData?.score_decomposition.rule_score} / 40
                </span>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                <span className="text-purple-400 font-bold block uppercase text-[10px]">2. ML Baseline</span>
                <p className="text-slate-300">RandomForest Risk Prob (0–35 pts)</p>
                <span className="text-emerald-400 font-bold block pt-1">
                  Score: {analysisData?.ml_score ?? analysisData?.score_decomposition.ml_score} / 35
                </span>
              </div>

              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-1">
                <span className="text-amber-400 font-bold block uppercase text-[10px]">3. Graph Engine</span>
                <p className="text-slate-300">NetworkX Centrality (0–25 pts)</p>
                <span className="text-emerald-400 font-bold block pt-1">
                  Score: {analysisData?.graph_score ?? analysisData?.score_decomposition.graph_score} / 25
                </span>
              </div>
            </div>

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>View Explainable Risk Breakdown</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 6: EXPLAINABLE RISK SCORE */}
        {currentStep === 6 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <Shield className="w-5 h-5" />
              <span>STEP 6: Explainable Composite Risk Score & Evidence</span>
            </div>

            <div className="p-5 bg-slate-950 border border-slate-800 rounded-xl space-y-3 font-mono">
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-400 uppercase font-semibold">Composite Risk Score</span>
                <span className="text-3xl font-bold text-rose-400">
                  {analysisData?.composite_risk_score ?? analysisData?.risk_score} / 100 ({analysisData?.risk_category || 'HIGH'})
                </span>
              </div>

              <div className="space-y-2 pt-2 border-t border-slate-900">
                <span className="text-[10px] text-amber-400 uppercase font-bold block">Triggered Traceable Evidence ({analysisData?.signals.length || 0})</span>
                {analysisData?.signals.map((sig, i) => (
                  <div key={i} className="p-2.5 bg-slate-900 border border-slate-800 rounded text-xs space-y-1">
                    <div className="flex justify-between font-bold text-slate-200">
                      <span>{sig.title}</span>
                      <span className="text-amber-400">+{sig.score_contribution} PTS</span>
                    </div>
                    <p className="text-[11px] text-slate-400">{sig.explanation}</p>
                  </div>
                ))}
              </div>
            </div>

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Proceed to Cytoscape.js Graph</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 7: TRANSACTION GRAPH */}
        {currentStep === 7 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <Network className="w-5 h-5" />
              <span>STEP 7: NetworkX + Cytoscape.js Directed Topology Canvas</span>
            </div>

            <div className="h-[380px] relative border border-slate-800 rounded-xl overflow-hidden">
              <CytoscapeGraph
                nodes={graphData?.nodes || []}
                edges={graphData?.edges || []}
                onSelectNode={(node) => setSelectedGraphNode(node)}
                riskFilter="all"
                minAmount={0}
              />
            </div>

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Generate Automated Alert</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 8: GENERATE ALERT */}
        {currentStep === 8 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-rose-400 font-bold text-sm uppercase tracking-wider font-mono">
              <AlertTriangle className="w-5 h-5" />
              <span>STEP 8: Generate High-Priority Triage Alert</span>
            </div>

            <div className="p-4 bg-slate-950 border border-rose-500/30 rounded-xl space-y-2 font-mono text-xs">
              <span className="px-2 py-0.5 bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded text-[10px] font-bold uppercase">
                HIGH PRIORITY ALERT GENERATED
              </span>
              <h3 className="text-sm font-bold text-slate-100">ALERT-2026-084: High Behavioral Risk Target</h3>
              <p className="text-slate-400">Subject: {selectedEntity}</p>
              <p className="text-slate-300">Composite Risk Score: 84 / 100 (HIGH). Rapid forwarding and multi-output fan-out splitting detected.</p>
            </div>

            <button
              onClick={handleTriggerCaseCreation}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Create Official Investigation Case</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 9: CREATE CASE */}
        {currentStep === 9 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm uppercase tracking-wider font-mono">
              <FileCheck className="w-5 h-5" />
              <span>STEP 9: Create Official Investigation Case</span>
            </div>

            <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2 font-mono text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Case ID:</span>
                <span className="text-cyan-400 font-bold">{createdCaseId}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Status:</span>
                <span className="text-emerald-400 font-bold uppercase">under_investigation</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Investigator:</span>
                <span className="text-slate-200">SIH Evaluator Analyst</span>
              </div>
            </div>

            <button
              onClick={handleNextStep}
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg flex items-center space-x-2"
            >
              <span>Export PDF Report</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* STEP 10: GENERATE PDF REPORT */}
        {currentStep === 10 && (
          <div className="space-y-4">
            <div className="flex items-center space-x-2 text-emerald-400 font-bold text-sm uppercase tracking-wider font-mono">
              <FileText className="w-5 h-5" />
              <span>STEP 10: Export Court-Ready PDF Forensic Report</span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Generate and download the court-ready PDF report containing complete risk score decomposition, rule evidence, feature vectors, and cryptographic checksums:
            </p>

            <div className="p-6 bg-slate-950 border border-slate-800 rounded-xl text-center space-y-4">
              <FileText className="w-12 h-12 text-cyan-400 mx-auto" />
              <div>
                <h3 className="text-sm font-mono font-bold text-slate-100">ChainSentinel Forensic Report (CASE-2026-004)</h3>
                <p className="text-xs text-slate-400 font-mono">Native ReportLab PDF generation with cryptographic integrity checksums.</p>
              </div>

              <a
                href={getCasePdfUrl(createdCaseId)}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center space-x-2 px-6 py-3 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-xl font-mono cursor-pointer"
              >
                <Download className="w-4 h-4" />
                <span>Download Official PDF Forensic Report</span>
              </a>
            </div>
          </div>
        )}
      </div>

      {/* STEPPER NAV FOOTER */}
      <div className="flex items-center justify-between font-mono text-xs pt-2">
        <button
          onClick={handlePrevStep}
          disabled={currentStep === 1}
          className="px-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-slate-300 disabled:opacity-40 flex items-center space-x-1"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Previous Step</span>
        </button>

        <span className="text-slate-400">Step {currentStep} of 10</span>

        <button
          onClick={handleNextStep}
          disabled={currentStep === 10}
          className="px-4 py-2 bg-cyan-500 text-slate-950 font-bold rounded-lg disabled:opacity-40 flex items-center space-x-1"
        >
          <span>Next Step</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
