import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Shield,
  Network,
  Download,
  PlusCircle,
  AlertTriangle,
  Loader2,
  Filter,
  Layers,
  Clock,
  ExternalLink,
  ChevronRight,
  X,
  PlayCircle,
  ArrowRight,
  Database
} from 'lucide-react';
import {
  fetchEntityGraph,
  analyzeAddress,
  fetchDemoScenarios,
  CytoscapeNodeData
} from '../services/api';
import { CytoscapeGraph } from '../components/CytoscapeGraph';

const DEFAULT_SUBJECT = 'bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0';

export const InvestigationPage: React.FC = () => {
  const { subjectId } = useParams<{ subjectId?: string }>();
  const activeSubject = subjectId || DEFAULT_SUBJECT;

  const [hops, setHops] = useState<number>(1);
  const [riskFilter, setRiskFilter] = useState<string>('all');
  const [minAmount, setMinAmount] = useState<number>(0);
  const [selectedNode, setSelectedNode] = useState<CytoscapeNodeData | null>(null);

  // Fetch Graph data dynamically from NetworkX + dataset or demo
  const { data: graphData, isLoading: isGraphLoading, isError: isGraphError } = useQuery({
    queryKey: ['entityGraph', activeSubject, hops, riskFilter],
    queryFn: () => fetchEntityGraph('address', activeSubject, hops, riskFilter),
  });

  // Fetch Risk Analysis data
  const { data: analysisData } = useQuery({
    queryKey: ['analyzeAddress', activeSubject],
    queryFn: () => analyzeAddress(activeSubject),
  });

  // Fetch Demo Scenarios for shortcut menu
  const { data: demoData } = useQuery({
    queryKey: ['demoScenarios'],
    queryFn: fetchDemoScenarios,
  });

  return (
    <div className="space-y-6">
      {/* Subject Header */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className={`px-2.5 py-0.5 text-[10px] font-mono uppercase font-bold rounded border ${
              analysisData?.risk_level === 'critical' ? 'bg-purple-500/10 text-purple-400 border-purple-500/30' :
              analysisData?.risk_level === 'high' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
              analysisData?.risk_level === 'medium' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
              'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
            }`}>
              {analysisData?.risk_level.toUpperCase() || 'HIGH'} RISK
            </span>
            <span className="text-xs text-slate-400 font-mono">Forensic Subject: Address</span>
            <span className="text-xs text-slate-500 font-mono">• Source: {analysisData?.data_source || 'Analyzed Dataset'}</span>
          </div>
          <h1 className="text-lg font-mono font-bold text-slate-100 mt-1 break-all flex items-center gap-2">
            <span>{activeSubject}</span>
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Load Demo Scenario Select Dropdown */}
          <div className="relative">
            <select
              onChange={(e) => {
                if (e.target.value) {
                  window.location.href = `/investigate/${e.target.value}`;
                }
              }}
              value={activeSubject}
              className="px-3 py-2 bg-slate-950 text-cyan-400 border border-slate-700 text-xs font-mono rounded-lg focus:outline-none focus:border-cyan-500"
            >
              <option value="" disabled>Load Demo Scenario...</option>
              {demoData?.scenarios.map((s) => (
                <option key={s.id} value={s.subject_id}>
                  {s.title} ({s.expected_score}/100)
                </option>
              ))}
            </select>
          </div>

          <button className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded-lg font-medium flex items-center space-x-2 border border-slate-700">
            <Download className="w-4 h-4 text-cyan-400" />
            <span>Export Report</span>
          </button>
          <button className="px-3.5 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs rounded-lg font-bold flex items-center space-x-2">
            <PlusCircle className="w-4 h-4" />
            <span>Create Case</span>
          </button>
        </div>
      </div>

      {/* Main Analysis Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Risk Gauge & Score Breakdown */}
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-6 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="text-center space-y-1">
              <span className="text-xs text-slate-400 uppercase tracking-wider font-semibold">Composite Risk Score</span>
              <div className={`text-5xl font-bold font-mono ${
                analysisData?.risk_level === 'critical' ? 'text-purple-400' :
                analysisData?.risk_level === 'high' ? 'text-rose-400' :
                analysisData?.risk_level === 'medium' ? 'text-amber-400' :
                'text-emerald-400'
              }`}>
                {analysisData?.risk_score || 84}<span className="text-lg text-slate-400">/100</span>
              </div>
              <div className="inline-block px-3 py-0.5 bg-rose-500/10 border border-rose-500/30 text-rose-400 rounded-full text-xs font-semibold uppercase">
                {analysisData?.risk_level.toUpperCase() || 'HIGH'} PRIORITY
              </div>
            </div>

            {/* Score Decomposition */}
            <div className="space-y-3 pt-4 border-t border-slate-800">
              <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Score Decomposition</h3>
              <div className="space-y-2.5 text-xs">
                <div>
                  <div className="flex justify-between text-slate-400 mb-1">
                    <span>Rule Engine Score</span>
                    <span className="font-mono text-slate-200">{(analysisData?.score_decomposition.rule_score || 35).toFixed(1)} / 40</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-cyan-400" style={{ width: `${((analysisData?.score_decomposition.rule_score || 35) / 40) * 100}%` }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-slate-400 mb-1">
                    <span>ML Baseline Score</span>
                    <span className="font-mono text-slate-200">{(analysisData?.score_decomposition.ml_score || 28).toFixed(1)} / 35</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-purple-400" style={{ width: `${((analysisData?.score_decomposition.ml_score || 28) / 35) * 100}%` }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-slate-400 mb-1">
                    <span>Graph Centrality Score</span>
                    <span className="font-mono text-slate-200">{(analysisData?.score_decomposition.graph_score || 21).toFixed(1)} / 25</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-amber-400" style={{ width: `${((analysisData?.score_decomposition.graph_score || 21) / 25) * 100}%` }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Recommended Action Box */}
          <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 space-y-1.5">
            <span className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider flex items-center space-x-1.5">
              <Shield className="w-4 h-4 text-cyan-400" />
              <span>Analyst Triage Protocol</span>
            </span>
            <p className="text-xs text-slate-300 leading-relaxed">
              {analysisData?.recommended_action || "PRIORITY HUMAN REVIEW: Conduct detailed multi-hop graph expansion."}
            </p>
          </div>
        </div>

        {/* Right 2 Columns: Directed Cytoscape Graph & Controls */}
        <div className="lg:col-span-2 space-y-6">
          {/* Cytoscape Container Panel */}
          <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4 relative">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <span className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
                <Network className="w-4 h-4 text-cyan-400" />
                <span>Transaction Topology Graph (NetworkX + Cytoscape.js)</span>
              </span>

              {/* Hop Selector & Risk Level Filters */}
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <div className="flex border border-slate-700 rounded-lg overflow-hidden bg-slate-950">
                  <button
                    onClick={() => setHops(1)}
                    className={`px-3 py-1 font-mono text-xs transition-colors ${
                      hops === 1 ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    1 Hop
                  </button>
                  <button
                    onClick={() => setHops(2)}
                    className={`px-3 py-1 font-mono text-xs transition-colors ${
                      hops === 2 ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    2 Hops
                  </button>
                </div>

                <select
                  value={riskFilter}
                  onChange={(e) => setRiskFilter(e.target.value)}
                  className="px-3 py-1 bg-slate-950 text-cyan-400 border border-slate-700 rounded-lg font-mono text-xs focus:outline-none"
                >
                  <option value="all">All Risks</option>
                  <option value="critical">Critical Only</option>
                  <option value="high">High Only</option>
                  <option value="medium">Medium Only</option>
                  <option value="low">Low Only</option>
                </select>
              </div>
            </div>

            {/* Truncation Alert Banner */}
            {graphData?.is_truncated && (
              <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-2.5 text-[11px] text-amber-300 flex items-center space-x-2">
                <AlertTriangle className="w-4 h-4 flex-shrink-0 text-amber-400" />
                <span>{graphData.truncation_message}</span>
              </div>
            )}

            {/* Canvas */}
            {isGraphLoading ? (
              <div className="h-[420px] flex items-center justify-center bg-slate-950 rounded-lg border border-slate-800">
                <div className="text-center space-y-2">
                  <Loader2 className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
                  <p className="text-xs text-slate-400 font-mono">Computing NetworkX PageRank & Topology...</p>
                </div>
              </div>
            ) : isGraphError ? (
              <div className="h-[420px] flex items-center justify-center bg-slate-950 rounded-lg border border-slate-800">
                <p className="text-xs text-rose-400 font-mono">Failed to render graph for {activeSubject}.</p>
              </div>
            ) : (
              <div className="h-[420px] relative">
                <CytoscapeGraph
                  nodes={graphData?.nodes || []}
                  edges={graphData?.edges || []}
                  onSelectNode={(node) => setSelectedNode(node)}
                  riskFilter={riskFilter}
                  minAmount={minAmount}
                />

                {/* Legend Overlay */}
                <div className="absolute bottom-3 left-3 bg-slate-950/90 backdrop-blur p-2.5 rounded-lg border border-slate-800 text-[10px] space-y-1 font-mono">
                  <div className="font-semibold text-slate-400 uppercase text-[9px]">Legend</div>
                  <div className="flex items-center space-x-3">
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500" /> Low</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-500" /> Medium</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-rose-500" /> High</span>
                    <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-purple-500" /> Critical</span>
                  </div>
                </div>
              </div>
            )}

            {/* Selected Node Details Drawer */}
            {selectedNode && (
              <div className="bg-slate-950 p-5 rounded-xl border border-cyan-500/40 space-y-4 shadow-xl">
                <div className="flex items-center justify-between border-b border-slate-800 pb-2.5">
                  <div className="flex items-center space-x-2">
                    <Database className="w-4 h-4 text-cyan-400" />
                    <span className="text-xs font-bold text-cyan-400 font-mono uppercase tracking-wider">
                      Selected Node Forensic Information
                    </span>
                  </div>
                  <button onClick={() => setSelectedNode(null)} className="text-slate-400 hover:text-slate-200">
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 text-xs font-mono">
                  <div className="col-span-2">
                    <span className="text-slate-500 block text-[10px] uppercase font-semibold">Address / Node ID</span>
                    <span className="text-slate-100 font-bold break-all">{selectedNode.id}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase font-semibold">Risk Score</span>
                    <span className={`font-bold text-sm ${
                      selectedNode.risk_level === 'critical' ? 'text-purple-400' :
                      selectedNode.risk_level === 'high' ? 'text-rose-400' :
                      selectedNode.risk_level === 'medium' ? 'text-amber-400' :
                      'text-emerald-400'
                    }`}>
                      {selectedNode.risk_score} / 100 ({selectedNode.risk_level.toUpperCase()})
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase font-semibold">In / Out Degree</span>
                    <span className="text-slate-200 font-bold">{selectedNode.metadata.in_degree} In / {selectedNode.metadata.out_degree} Out</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase font-semibold">Transaction Count</span>
                    <span className="text-slate-200 font-bold">{selectedNode.metadata.tx_count || (selectedNode.metadata.in_degree + selectedNode.metadata.out_degree)}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase font-semibold">Volume (BTC)</span>
                    <span className="text-cyan-400 font-bold">{(selectedNode.metadata.volume_btc || selectedNode.amount_btc || 0.0).toFixed(4)} BTC</span>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono pt-2 border-t border-slate-900">
                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase font-semibold">NetworkX PageRank</span>
                    <span className="text-slate-300 font-bold">{selectedNode.metadata.pagerank}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px] uppercase font-semibold">Dist. to Flagged Cluster</span>
                    <span className="text-slate-300 font-bold">
                      {selectedNode.metadata.shortest_distance_to_flagged !== null ? `${selectedNode.metadata.shortest_distance_to_flagged} Hop(s)` : 'Direct / Unlinked'}
                    </span>
                  </div>
                </div>

                {/* Triggered Behavioral Indicators */}
                {selectedNode.metadata.signals && selectedNode.metadata.signals.length > 0 && (
                  <div className="pt-2 border-t border-slate-900 space-y-1.5">
                    <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider block">
                      Triggered Behavioral Risk Indicators ({selectedNode.metadata.signals.length})
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedNode.metadata.signals.map((sigTitle, i) => (
                        <span key={i} className="px-2 py-0.5 bg-amber-500/10 text-amber-300 border border-amber-500/30 text-[10px] font-mono rounded">
                          {sigTitle}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Behavioral Evidence Cards Row */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
          <AlertTriangle className="w-4 h-4 text-amber-400" />
          <span>Structured Evidence Cards ({analysisData?.signals.length || 0})</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {analysisData?.signals.map((sig, idx) => (
            <div key={idx} className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-200">{sig.title}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                  sig.severity === 'critical' ? 'bg-purple-500/10 text-purple-400 border-purple-500/30' :
                  sig.severity === 'high' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                  sig.severity === 'medium' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
                  'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                }`}>
                  +{sig.score_contribution} PTS
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{sig.explanation}</p>
              <div className="text-[11px] text-cyan-300 flex items-start space-x-1.5">
                <ArrowRight className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-cyan-400" />
                <span>{sig.recommended_review_step}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
