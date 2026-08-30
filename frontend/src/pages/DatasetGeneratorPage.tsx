import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useNavigate } from 'react-router-dom';
import {
  Database,
  Download,
  Play,
  CheckCircle2,
  AlertTriangle,
  FileSpreadsheet,
  Settings,
  RefreshCw,
  Loader2,
  ChevronRight,
  ShieldAlert,
  Sliders,
  FileText,
  Upload,
  FileCode,
  FileCheck,
  Lock,
  ArrowRight
} from 'lucide-react';
import {
  generateSyntheticDataset,
  uploadDatasetFile,
  validateDatasetFile,
  getDatasetDownloadUrl,
  GenerateDatasetResponse,
  DatasetExplorerResponse,
  DatasetValidationReport
} from '../services/api';

export const DatasetGeneratorPage: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [activeTab, setActiveTab] = useState<'upload' | 'generate' | 'demo'>('upload');
  
  // File Upload State
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationReport, setValidationReport] = useState<DatasetValidationReport | null>(null);
  const [uploadResult, setUploadResult] = useState<DatasetExplorerResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Generator State
  const [numRecords, setNumRecords] = useState<number>(100);
  const [seed, setSeed] = useState<number>(42);
  const [generatedMeta, setGeneratedMeta] = useState<GenerateDatasetResponse | null>(null);

  const [probNormal, setProbNormal] = useState<number>(0.40);
  const [probRapid, setProbRapid] = useState<number>(0.10);
  const [probFanOut, setProbFanOut] = useState<number>(0.10);
  const [probFanIn, setProbFanIn] = useState<number>(0.10);
  const [probPeel, setProbPeel] = useState<number>(0.08);
  const [probCycle, setProbCycle] = useState<number>(0.06);
  const [probDormant, setProbDormant] = useState<number>(0.06);
  const [probSmurf, setProbSmurf] = useState<number>(0.05);
  const [probNeighbor, setProbNeighbor] = useState<number>(0.05);

  const validateMutation = useMutation({
    mutationFn: validateDatasetFile,
    onSuccess: (data) => {
      setValidationReport(data);
      setErrorMessage(null);
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Validation failed. Check file formatting.');
    }
  });

  const uploadMutation = useMutation({
    mutationFn: uploadDatasetFile,
    onSuccess: (data) => {
      setUploadResult(data);
      setErrorMessage(null);
      queryClient.invalidateQueries({ queryKey: ['dashboardSummary'] });
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Failed to upload and analyze dataset file.');
    }
  });

  const generateMutation = useMutation({
    mutationFn: generateSyntheticDataset,
    onSuccess: (data) => {
      setGeneratedMeta(data);
      setErrorMessage(null);
      queryClient.invalidateQueries({ queryKey: ['dashboardSummary'] });
    },
    onError: (err: any) => {
      setErrorMessage(err.response?.data?.detail || 'Failed to generate synthetic dataset.');
    }
  });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setValidationReport(null);
      setUploadResult(null);
      setErrorMessage(null);
    }
  };

  const handleValidateClick = () => {
    if (selectedFile) {
      validateMutation.mutate(selectedFile);
    }
  };

  const handleAnalyzeClick = () => {
    if (selectedFile) {
      uploadMutation.mutate(selectedFile);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-xl border border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-3">
            <span>Dataset Management Terminal</span>
            <span className="text-xs font-mono font-normal px-2.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              SIH26146
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Upload custom transaction datasets (CSV, JSON, TXT), generate reproducible synthetic traffic, or load SIH judging demo sets.
          </p>
        </div>

        <div className="flex items-center space-x-2 font-mono text-xs">
          <Link
            to="/explorer"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-300 font-semibold rounded-lg border border-slate-700 flex items-center gap-1.5"
          >
            <Database className="w-4 h-4 text-cyan-400" />
            <span>Dataset Explorer</span>
          </Link>
        </div>
      </div>

      {/* Tab Controls */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-3 font-mono text-xs">
        <button
          onClick={() => setActiveTab('upload')}
          className={`px-4 py-2.5 rounded-lg font-bold flex items-center gap-2 transition-colors border ${
            activeTab === 'upload'
              ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/30'
              : 'bg-slate-900/60 text-slate-400 border-slate-800 hover:bg-slate-800'
          }`}
        >
          <Upload className="w-4 h-4" />
          <span>Upload Data File (CSV / JSON / TXT)</span>
        </button>

        <button
          onClick={() => setActiveTab('generate')}
          className={`px-4 py-2.5 rounded-lg font-bold flex items-center gap-2 transition-colors border ${
            activeTab === 'generate'
              ? 'bg-purple-500/10 text-purple-400 border-purple-500/30'
              : 'bg-slate-900/60 text-slate-400 border-slate-800 hover:bg-slate-800'
          }`}
        >
          <Sliders className="w-4 h-4" />
          <span>Synthetic Dataset Generator</span>
        </button>
      </div>

      {/* ERROR MESSAGE ALERT */}
      {errorMessage && (
        <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4 text-rose-400 text-xs font-mono flex items-center space-x-2">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* UPLOAD TAB CONTENT */}
      {activeTab === 'upload' && (
        <div className="space-y-6">
          <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-sm font-bold font-mono text-slate-200 uppercase tracking-wider flex items-center gap-2">
                  <Upload className="w-4 h-4 text-cyan-400" />
                  <span>Upload Custom Bitcoin Transaction Dataset</span>
                </h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Supported Formats: <span className="text-cyan-400 font-mono font-bold">CSV • JSON • TXT</span> (Max file size: 10 MB)
                </p>
              </div>

              <div className="px-3 py-1 bg-amber-500/10 border border-amber-500/30 text-amber-400 rounded text-[11px] font-mono flex items-center gap-1.5">
                <Lock className="w-3.5 h-3.5" />
                <span>Read-Only Analytics (No Credentials)</span>
              </div>
            </div>

            {/* SECURITY WARNING BANNER */}
            <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-400 flex items-center space-x-2">
              <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0" />
              <span>ChainSentinel is a read-only risk analytics platform. Never upload private keys, wallet seed phrases, or credentials.</span>
            </div>

            {/* FILE UPLOAD DROP ZONE */}
            <div className="p-8 border-2 border-dashed border-slate-700 hover:border-cyan-500/50 bg-slate-950/60 rounded-xl text-center space-y-4 transition-colors">
              <FileCode className="w-12 h-12 text-cyan-400 mx-auto animate-pulse" />
              <div className="space-y-1">
                <h3 className="text-sm font-bold font-mono text-slate-100">Select or Drag Transaction File</h3>
                <p className="text-xs text-slate-400 font-mono">Supports standard CSV, JSON transaction arrays, or delimiter-separated TXT logs.</p>
              </div>

              <label className="inline-flex items-center space-x-2 px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs font-mono rounded-lg cursor-pointer transition-colors">
                <Upload className="w-4 h-4" />
                <span>Choose File</span>
                <input
                  type="file"
                  accept=".csv,.json,.txt"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </label>
            </div>

            {/* SELECTED FILE PREVIEW & DETAILS */}
            {selectedFile && (
              <div className="p-5 bg-slate-950 border border-slate-800 rounded-xl space-y-4 font-mono text-xs">
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">File Name</span>
                    <span className="text-cyan-400 font-bold truncate block">{selectedFile.name}</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">File Type</span>
                    <span className="text-purple-400 font-bold uppercase">{selectedFile.name.split('.').pop()}</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">File Size</span>
                    <span className="text-slate-200 font-bold">{(selectedFile.size / 1024).toFixed(1)} KB</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">Validation Status</span>
                    <span className={`font-bold uppercase ${
                      validationReport?.is_valid ? 'text-emerald-400' : validationReport ? 'text-rose-400' : 'text-amber-400'
                    }`}>
                      {validationReport ? (validationReport.is_valid ? 'VALID' : 'INVALID') : 'NOT VALIDATED'}
                    </span>
                  </div>
                </div>

                {/* VALIDATION MESSAGES IF PRESENT */}
                {validationReport && (
                  <div className="p-3 bg-slate-900 border border-slate-800 rounded space-y-2">
                    <div className="flex justify-between items-center text-xs font-bold">
                      <span className="text-slate-300">Checked Records: {validationReport.total_rows_checked}</span>
                      <span className={validationReport.is_valid ? 'text-emerald-400' : 'text-rose-400'}>
                        {validationReport.error_count} Errors / {validationReport.warnings.length} Warnings
                      </span>
                    </div>

                    {validationReport.errors.map((err, i) => (
                      <p key={i} className="text-rose-400 text-[11px] font-mono">
                        • {err.message}
                      </p>
                    ))}
                    {validationReport.warnings.map((warn, i) => (
                      <p key={i} className="text-amber-400 text-[11px] font-mono">
                        • {warn}
                      </p>
                    ))}
                  </div>
                )}

                {/* ACTION BUTTONS */}
                <div className="flex items-center space-x-3 pt-2">
                  <button
                    onClick={handleValidateClick}
                    disabled={validateMutation.isPending}
                    className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold rounded-lg border border-slate-700 flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {validateMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin text-cyan-400" /> : <FileCheck className="w-4 h-4 text-cyan-400" />}
                    <span>Validate Dataset</span>
                  </button>

                  <button
                    onClick={handleAnalyzeClick}
                    disabled={uploadMutation.isPending}
                    className="px-5 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-lg flex items-center gap-1.5 disabled:opacity-50"
                  >
                    {uploadMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin text-slate-950" /> : <Play className="w-4 h-4 text-slate-950" />}
                    <span>Analyze Dataset & Update Dashboard</span>
                  </button>
                </div>
              </div>
            )}

            {/* SUCCESS ANALYSIS SUMMARY DISPLAY */}
            {uploadResult && (
              <div className="p-6 bg-slate-950 border border-emerald-500/40 rounded-xl space-y-4 font-mono text-xs">
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <div className="flex items-center space-x-2">
                    <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    <h3 className="font-bold text-slate-100 text-sm">Dataset Uploaded & Analyzed Successfully!</h3>
                  </div>
                  <span className="px-2.5 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded text-[10px] uppercase font-bold">
                    ACTIVE DATASET UPDATED
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">Total Transactions</span>
                    <span className="text-lg font-bold text-slate-100">{uploadResult.summary.total_transactions}</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">Unique Addresses</span>
                    <span className="text-lg font-bold text-cyan-400">{uploadResult.summary.unique_addresses}</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">Total Volume BTC</span>
                    <span className="text-lg font-bold text-emerald-400">{uploadResult.summary.total_volume_btc.toFixed(2)} BTC</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">Avg Tx Amount</span>
                    <span className="text-lg font-bold text-purple-400">{uploadResult.summary.avg_transaction_amount_btc.toFixed(3)} BTC</span>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-2">
                  <Link
                    to="/dashboard"
                    className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-lg flex items-center gap-1.5 cursor-pointer"
                  >
                    <span>View Dynamic Dashboard</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>

                  <Link
                    to="/explorer"
                    className="text-cyan-400 hover:underline flex items-center gap-1"
                  >
                    <span>Explore Dataset Table</span>
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* GENERATE TAB CONTENT */}
      {activeTab === 'generate' && (
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-6 font-mono text-xs">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
                <Sliders className="w-4 h-4 text-purple-400" />
                <span>Synthetic Bitcoin Transaction Generator</span>
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">Configure record count, random seed, and controlled behavioral scenario distributions.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-slate-400 text-[11px] uppercase font-bold block">Record Count</label>
              <input
                type="number"
                value={numRecords}
                onChange={(e) => setNumRecords(parseInt(e.target.value) || 100)}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded text-slate-100 font-bold"
              />
            </div>
            <div className="space-y-2">
              <label className="text-slate-400 text-[11px] uppercase font-bold block">Random Seed (Reproducible)</label>
              <input
                type="number"
                value={seed}
                onChange={(e) => setSeed(parseInt(e.target.value) || 42)}
                className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded text-slate-100 font-bold"
              />
            </div>
          </div>

          <button
            onClick={() => generateMutation.mutate({
              num_records: numRecords,
              seed: seed,
              scenario_distribution: {
                normal: probNormal,
                rapid_forwarding: probRapid,
                fan_out: probFanOut,
                fan_in: probFanIn,
                peeling_chain: probPeel,
                circular_flow: probCycle,
                dormancy_burst: probDormant,
                structuring: probSmurf,
                risky_neighbor: probNeighbor
              }
            })}
            disabled={generateMutation.isPending}
            className="px-5 py-2.5 bg-purple-500 hover:bg-purple-400 text-slate-950 font-bold rounded-lg flex items-center gap-2 disabled:opacity-50 cursor-pointer"
          >
            {generateMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin text-slate-950" /> : <Play className="w-4 h-4 text-slate-950" />}
            <span>Generate & Activate Synthetic Dataset</span>
          </button>

          {generatedMeta && (
            <div className="p-6 bg-slate-950 border border-purple-500/40 rounded-xl space-y-4 font-mono text-xs mt-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center space-x-2">
                  <CheckCircle2 className="w-5 h-5 text-purple-400" />
                  <h3 className="font-bold text-slate-100 text-sm">Synthetic Dataset Generated & Activated!</h3>
                </div>
                <span className="px-2.5 py-0.5 bg-purple-500/10 text-purple-400 border border-purple-500/30 rounded text-[10px] uppercase font-bold">
                  ACTIVE DATASET UPDATED
                </span>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                  <span className="text-slate-500 text-[10px] block uppercase">Total Transactions</span>
                  <span className="text-lg font-bold text-slate-100">{generatedMeta.num_records}</span>
                </div>
                <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                  <span className="text-slate-500 text-[10px] block uppercase">Random Seed</span>
                  <span className="text-lg font-bold text-cyan-400">{generatedMeta.seed}</span>
                </div>
                <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                  <span className="text-slate-500 text-[10px] block uppercase">Active File</span>
                  <span className="text-xs font-bold text-purple-400 truncate block">{generatedMeta.filename}</span>
                </div>
                <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                  <span className="text-slate-500 text-[10px] block uppercase">Status</span>
                  <span className="text-xs font-bold text-emerald-400 uppercase">ACTIVE</span>
                </div>
              </div>

              <div className="flex items-center justify-between pt-2">
                <Link
                  to="/dashboard"
                  className="px-4 py-2 bg-purple-500 hover:bg-purple-400 text-slate-950 font-bold rounded-lg flex items-center gap-1.5 cursor-pointer"
                >
                  <span>View Dynamic Dashboard</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>

                <Link
                  to="/explorer"
                  className="text-cyan-400 hover:underline flex items-center gap-1"
                >
                  <span>Explore Dataset Table</span>
                  <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
