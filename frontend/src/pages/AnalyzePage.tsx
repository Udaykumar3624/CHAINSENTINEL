import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  Search,
  Upload,
  Database,
  AlertTriangle,
  Shield,
  Loader2,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  FileSpreadsheet,
  RefreshCw,
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import {
  analyzeAddress,
  analyzeTransaction,
  analyzeCsv,
  fetchDemoScenarios,
  AnalysisResultResponse,
  CsvAnalysisBatchResponse,
  DemoScenarioItem
} from '../services/api';

export const AnalyzePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'address' | 'tx' | 'csv' | 'scenario'>('address');
  const [addressInput, setAddressInput] = useState('');
  const [txInput, setTxInput] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  const [analysisResult, setAnalysisResult] = useState<AnalysisResultResponse | null>(null);
  const [csvResult, setCsvResult] = useState<CsvAnalysisBatchResponse | null>(null);

  // Fetch demo scenarios
  const { data: demoData } = useQuery({
    queryKey: ['demoScenarios'],
    queryFn: fetchDemoScenarios,
  });

  // Mutations
  const addressMutation = useMutation({
    mutationFn: analyzeAddress,
    onSuccess: (data) => {
      setAnalysisResult(data);
      setCsvResult(null);
      setValidationError(null);
    },
    onError: (err: any) => {
      setValidationError(err.response?.data?.detail || 'Failed to analyze address. Please verify address format.');
    },
  });

  const txMutation = useMutation({
    mutationFn: analyzeTransaction,
    onSuccess: (data) => {
      setAnalysisResult(data);
      setCsvResult(null);
      setValidationError(null);
    },
    onError: (err: any) => {
      setValidationError(err.response?.data?.detail || 'Failed to analyze transaction. Please verify TxID format.');
    },
  });

  const csvMutation = useMutation({
    mutationFn: analyzeCsv,
    onSuccess: (data) => {
      setCsvResult(data);
      setAnalysisResult(null);
      setValidationError(null);
    },
    onError: (err: any) => {
      setValidationError(err.response?.data?.detail || 'Failed to parse CSV batch file.');
    },
  });

  const handleAnalyzeAddress = (e: React.FormEvent) => {
    e.preventDefault();
    if (!addressInput.trim()) {
      setValidationError('Please enter a Bitcoin address.');
      return;
    }
    setValidationError(null);
    addressMutation.mutate(addressInput.trim());
  };

  const handleAnalyzeTx = (e: React.FormEvent) => {
    e.preventDefault();
    if (!txInput.trim()) {
      setValidationError('Please enter a 64-character transaction ID.');
      return;
    }
    setValidationError(null);
    txMutation.mutate(txInput.trim());
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (!file.name.toLowerCase().endsWith('.csv')) {
        setValidationError('Invalid file type. Please select a .csv file.');
        setSelectedFile(null);
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        setValidationError('File size exceeds 10 MB limit.');
        setSelectedFile(null);
        return;
      }
      setValidationError(null);
      setSelectedFile(file);
    }
  };

  const handleUploadCsv = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) {
      setValidationError('Please select a valid .csv file to upload.');
      return;
    }
    setValidationError(null);
    csvMutation.mutate(selectedFile);
  };

  const handleSelectScenario = (scenario: DemoScenarioItem) => {
    setValidationError(null);
    if (scenario.subject_type === 'address') {
      addressMutation.mutate(scenario.subject_id);
    } else {
      txMutation.mutate(scenario.subject_id);
    }
  };

  const isLoading = addressMutation.isPending || txMutation.isPending || csvMutation.isPending;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-2">
        <div className="flex items-center justify-between">
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Search className="w-5 h-5 text-cyan-400" />
            <span>Explainable Bitcoin Risk Analysis Terminal</span>
          </h1>
          <span className="px-2.5 py-0.5 text-[11px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 rounded flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
            <span>Data Source: Live & Demo Engine (SIH26146)</span>
          </span>
        </div>
        <p className="text-xs text-slate-400">
          Enter a Bitcoin address, transaction ID, or upload CSV logs to generate transparent, 10-indicator behavioral risk scores.
        </p>

        {/* Tabs */}
        <div className="flex border-b border-slate-800 pt-4 space-x-4">
          {[
            { id: 'address', label: 'Address Lookup', icon: Search },
            { id: 'tx', label: 'Transaction ID', icon: Search },
            { id: 'csv', label: 'Batch CSV Upload', icon: Upload },
            { id: 'scenario', label: 'Demo Scenarios', icon: Database },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id as any);
                  setValidationError(null);
                }}
                className={`pb-3 text-xs font-medium border-b-2 flex items-center space-x-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-cyan-400 text-cyan-400'
                    : 'border-transparent text-slate-400 hover:text-slate-200'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Input Forms */}
        <div className="pt-4 space-y-4">
          {activeTab === 'address' && (
            <form onSubmit={handleAnalyzeAddress} className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                placeholder="Enter BTC Address (e.g., bc1q9x087v2n... or 1A1zP...)"
                value={addressInput}
                onChange={(e) => setAddressInput(e.target.value)}
                className="flex-1 px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
              />
              <button
                type="submit"
                disabled={isLoading}
                className="px-6 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs rounded-lg transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                <span>Analyze Address</span>
              </button>
            </form>
          )}

          {activeTab === 'tx' && (
            <form onSubmit={handleAnalyzeTx} className="flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                placeholder="Enter 64-character Transaction Hash (TxID)"
                value={txInput}
                onChange={(e) => setTxInput(e.target.value)}
                className="flex-1 px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
              />
              <button
                type="submit"
                disabled={isLoading}
                className="px-6 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs rounded-lg transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
                <span>Analyze Transaction</span>
              </button>
            </form>
          )}

          {activeTab === 'csv' && (
            <form onSubmit={handleUploadCsv} className="space-y-4">
              <div className="border-2 border-dashed border-slate-800 hover:border-cyan-500/50 rounded-xl p-8 text-center space-y-3 bg-slate-950/40 transition-colors">
                <FileSpreadsheet className="w-10 h-10 text-cyan-400 mx-auto" />
                <div className="space-y-1">
                  <p className="text-xs text-slate-200 font-medium">Upload CSV containing tx_hash, source_address, destination_address, amount_btc, timestamp</p>
                  <p className="text-[11px] text-slate-400">Max file size: 10 MB • Up to 10,000 transaction rows</p>
                </div>
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  className="hidden"
                  id="csv-file-input"
                />
                <div className="flex justify-center items-center gap-3">
                  <label htmlFor="csv-file-input" className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs rounded-lg cursor-pointer font-medium border border-slate-700">
                    Browse CSV File
                  </label>
                  {selectedFile && (
                    <span className="text-xs font-mono text-cyan-400 font-semibold">{selectedFile.name} ({(selectedFile.size / 1024).toFixed(1)} KB)</span>
                  )}
                </div>
              </div>
              {selectedFile && (
                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs rounded-lg transition-colors flex items-center justify-center space-x-2"
                >
                  {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}
                  <span>Run Batch Risk Analysis</span>
                </button>
              )}
            </form>
          )}

          {activeTab === 'scenario' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {demoData?.scenarios.map((scenario) => (
                <button
                  key={scenario.id}
                  onClick={() => handleSelectScenario(scenario)}
                  className="p-4 bg-slate-950 border border-slate-800 hover:border-cyan-500/40 rounded-lg text-left space-y-2 transition-all"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-200">{scenario.title}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                      {scenario.expected_score}/100
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 line-clamp-2">{scenario.description}</p>
                </button>
              ))}
            </div>
          )}

          {/* Validation & Live Lookup Error Banner */}
          {validationError && (
            <div className="bg-rose-500/10 border border-rose-500/30 rounded-lg p-3.5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-rose-400 text-xs">
              <div className="flex items-start space-x-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <div className="space-y-0.5">
                  <span className="font-semibold text-rose-300">Analysis Lookup Notice</span>
                  <p className="text-[11px] text-rose-400/90">{validationError}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2 w-full sm:w-auto justify-end">
                <button
                  onClick={() => {
                    setActiveTab('scenario');
                    setValidationError(null);
                  }}
                  className="px-3 py-1.5 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 font-semibold text-xs rounded border border-cyan-500/40 transition-colors"
                >
                  Switch to Demo Mode
                </button>
                <button onClick={() => setValidationError(null)} className="text-xs font-mono underline hover:text-rose-300 px-2 py-1">
                  Dismiss
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Analysis Result Output View */}
      {analysisResult && (
        <div className="space-y-6">
          {/* Top Panel: Subject & Score */}
          <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 flex flex-col lg:flex-row justify-between gap-6">
            <div className="space-y-3 flex-1">
              <div className="flex items-center space-x-2">
                <span className={`px-2.5 py-0.5 text-[10px] font-mono uppercase font-bold rounded border ${
                  analysisResult.risk_level === 'critical' ? 'bg-purple-500/10 text-purple-400 border-purple-500/30' :
                  analysisResult.risk_level === 'high' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                  analysisResult.risk_level === 'medium' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
                  'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                }`}>
                  CATEGORY: {analysisResult.risk_category || analysisResult.risk_level.toUpperCase()}
                </span>
                <span className="text-xs text-slate-400 font-mono">Subject: {analysisResult.subject_type.toUpperCase()}</span>
                <span className="text-xs text-slate-500 font-mono">• Source: {analysisResult.data_source}</span>
                {analysisResult.is_ml_fallback && (
                  <span className="px-2 py-0.5 text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded">
                    ML Fallback Mode
                  </span>
                )}
              </div>

              <h2 className="text-lg font-mono font-bold text-slate-100 break-all">
                {analysisResult.subject_id}
              </h2>

              {/* Recommended Action */}
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 flex items-start space-x-3">
                <Shield className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <span className="text-[11px] font-bold text-cyan-400 uppercase tracking-wider">Recommended Analyst Action</span>
                  <p className="text-xs text-slate-300 leading-relaxed">{analysisResult.recommended_action}</p>
                </div>
              </div>
            </div>

            {/* Score Breakdown Column */}
            <div className="w-full lg:w-80 bg-slate-950 p-5 rounded-xl border border-slate-800 space-y-4 flex flex-col justify-between">
              <div className="text-center space-y-1">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Composite Risk Score</span>
                <div className={`text-4xl font-bold font-mono ${
                  analysisResult.risk_level === 'critical' ? 'text-purple-400' :
                  analysisResult.risk_level === 'high' ? 'text-rose-400' :
                  analysisResult.risk_level === 'medium' ? 'text-amber-400' :
                  'text-emerald-400'
                }`}>
                  {analysisResult.composite_risk_score ?? analysisResult.risk_score}<span className="text-base text-slate-400">/100</span>
                </div>
              </div>

              <div className="space-y-2.5 text-xs">
                <div>
                  <div className="flex justify-between text-slate-400 mb-1">
                    <span>Rule Engine Score</span>
                    <span className="font-mono text-slate-200">
                      {(analysisResult.rule_score ?? analysisResult.score_decomposition.rule_score).toFixed(1)} / 40
                    </span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-cyan-400" style={{ width: `${((analysisResult.rule_score ?? analysisResult.score_decomposition.rule_score) / 40) * 100}%` }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-slate-400 mb-1">
                    <span>ML Baseline Score</span>
                    <span className="font-mono text-slate-200">
                      {(analysisResult.ml_score ?? analysisResult.score_decomposition.ml_score).toFixed(1)} / 35
                    </span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-purple-400" style={{ width: `${((analysisResult.ml_score ?? analysisResult.score_decomposition.ml_score) / 35) * 100}%` }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between text-slate-400 mb-1">
                    <span>Graph Engine Score</span>
                    <span className="font-mono text-slate-200">
                      {(analysisResult.graph_score ?? analysisResult.score_decomposition.graph_score).toFixed(1)} / 25
                    </span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-amber-400" style={{ width: `${((analysisResult.graph_score ?? analysisResult.score_decomposition.graph_score) / 25) * 100}%` }}></div>
                  </div>
                </div>
              </div>

              <Link
                to={`/investigate/${analysisResult.subject_id}`}
                className="w-full py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg transition-colors flex items-center justify-center space-x-2"
              >
                <span>Launch Graph Investigation</span>
                <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          </div>

          {/* Computed Feature Values Matrix */}
          {analysisResult.feature_values && (
            <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
                <Database className="w-4 h-4 text-cyan-400" />
                <span>Extracted Feature Vector Values</span>
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-2.5 font-mono text-[11px]">
                {Object.entries(analysisResult.feature_values).map(([fk, fv]) => (
                  <div key={fk} className="p-2.5 bg-slate-950 border border-slate-800/80 rounded-lg">
                    <span className="text-slate-500 block text-[9px] uppercase truncate">{fk}</span>
                    <span className="text-slate-200 font-bold truncate block">{String(fv)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Behavioral Signals & Evidence Grid */}
          <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              <span>Traceable Evidence & Triggered Indicators ({(analysisResult.evidence || analysisResult.signals).length})</span>
            </h3>

            {(analysisResult.evidence || analysisResult.signals).length === 0 ? (
              <div className="p-6 bg-slate-950 border border-slate-800 rounded-lg text-center text-xs text-slate-400">
                No high-risk behavioral indicators triggered. Subject exhibits standard retail transaction patterns.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {(analysisResult.evidence || analysisResult.signals).map((sig, idx) => (
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

                    <div className="bg-slate-900/80 p-2.5 rounded border border-slate-800/80 text-[11px] font-mono space-y-1">
                      <span className="text-slate-400 block text-[10px] uppercase tracking-wider font-semibold">Observed Evidence</span>
                      {Object.entries(sig.observed_values).map(([k, v]) => (
                        <div key={k} className="flex justify-between text-slate-300">
                          <span className="text-slate-400">{k}:</span>
                          <span>{String(v)}</span>
                        </div>
                      ))}
                    </div>

                    <div className="text-[11px] text-cyan-300 flex items-start space-x-1.5 pt-1">
                      <ArrowRight className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-cyan-400" />
                      <span>{sig.recommended_review_step}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* CSV Batch Results View */}
      {csvResult && (
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-6">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
            <div>
              <span className="text-[10px] font-mono font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 border border-amber-500/30 rounded uppercase tracking-wider">
                {csvResult.data_source_label || "DATA SOURCE: USER-UPLOADED SYNTHETIC DATA"}
              </span>
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2 mt-2">
                <FileSpreadsheet className="w-5 h-5 text-cyan-400" />
                <span>Batch CSV Analysis: {csvResult.filename}</span>
              </h2>
            </div>
            <div className="flex space-x-2 font-mono text-xs">
              <span className="px-2.5 py-1 bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded font-bold">
                High Risk: {csvResult.high_risk_count}
              </span>
              <span className="px-2.5 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded font-bold">
                Medium Risk: {csvResult.medium_risk_count}
              </span>
              <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded font-bold">
                Low Risk: {csvResult.low_risk_count}
              </span>
            </div>
          </div>

          {/* Dataset Summary Cards (Calculated directly from uploaded file) */}
          {csvResult.summary && (
            <div className="space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                Uploaded Dataset Summary (Derived Directly from File)
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-400 text-[10px] block uppercase">Total Records</span>
                  <span className="text-slate-100 font-bold text-sm">{csvResult.summary.total_records} rows</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-400 text-[10px] block uppercase">Unique Addresses</span>
                  <span className="text-cyan-400 font-bold text-sm">{csvResult.summary.unique_addresses}</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-400 text-[10px] block uppercase">Total Volume</span>
                  <span className="text-emerald-400 font-bold text-sm">{csvResult.summary.total_volume_btc.toFixed(2)} BTC</span>
                </div>
                <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg">
                  <span className="text-slate-400 text-[10px] block uppercase">Data Quality</span>
                  <span className="text-slate-200 font-bold text-xs block">
                    {csvResult.summary.missing_values_count} Missing • {csvResult.summary.duplicate_records_count} Dups
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Feature Extraction & Risk Results Table */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Extracted Feature Matrix & Risk Analysis Results
            </h3>
            <div className="overflow-x-auto border border-slate-800 rounded-xl">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950 border-b border-slate-800 text-slate-400 font-mono uppercase text-[10px]">
                  <tr>
                    <th className="px-4 py-3">Row</th>
                    <th className="px-4 py-3">Tx Hash</th>
                    <th className="px-4 py-3">Source Address</th>
                    <th className="px-4 py-3">Amount</th>
                    <th className="px-4 py-3">PageRank</th>
                    <th className="px-4 py-3">In/Out Deg</th>
                    <th className="px-4 py-3">Cycle</th>
                    <th className="px-4 py-3">Risk Score</th>
                    <th className="px-4 py-3">Top Signal</th>
                    <th className="px-4 py-3">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {csvResult.results.map((row) => (
                    <tr key={row.row_index} className="hover:bg-slate-800/30 transition-colors">
                      <td className="px-4 py-3 text-slate-400">#{row.row_index}</td>
                      <td className="px-4 py-3 text-slate-200 max-w-[130px] truncate">{row.tx_hash}</td>
                      <td className="px-4 py-3 text-cyan-400 max-w-[150px] truncate">{row.source_address}</td>
                      <td className="px-4 py-3 text-slate-200">{row.amount_btc.toFixed(4)} BTC</td>
                      <td className="px-4 py-3 text-slate-300">{(row.pagerank || 0.0).toFixed(4)}</td>
                      <td className="px-4 py-3 text-slate-400">{row.in_degree || 0} / {row.out_degree || 0}</td>
                      <td className="px-4 py-3">
                        {row.has_cycle ? (
                          <span className="px-1.5 py-0.5 bg-rose-500/20 text-rose-300 text-[10px] rounded font-bold">YES</span>
                        ) : (
                          <span className="text-slate-500 text-[10px]">NO</span>
                        )}
                      </td>
                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded font-bold border ${
                          row.risk_level === 'critical' ? 'bg-purple-500/10 text-purple-400 border-purple-500/30' :
                          row.risk_level === 'high' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                          row.risk_level === 'medium' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
                          'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                        }`}>
                          {row.risk_score} ({row.risk_level.toUpperCase()})
                        </span>
                      </td>
                      <td className="px-4 py-3 text-slate-300 font-sans">{row.top_signal}</td>
                      <td className="px-4 py-3 font-sans">
                        <Link
                          to={`/investigate/${row.source_address || row.tx_hash}`}
                          className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-cyan-400 text-[11px] rounded border border-slate-700 inline-flex items-center gap-1"
                        >
                          <span>Investigate</span>
                          <ChevronRight className="w-3 h-3" />
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
