import React, { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Database,
  Search,
  Filter,
  ArrowUpDown,
  FileSpreadsheet,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Layers,
  ChevronLeft,
  ChevronRight,
  Loader2,
  Table,
  Cpu
} from 'lucide-react';
import { fetchDatasetExplorer, DatasetAnalysisResultItem } from '../services/api';

export const DatasetExplorerPage: React.FC = () => {
  const { data: explorerData, isLoading, isError } = useQuery({
    queryKey: ['datasetExplorer'],
    queryFn: () => fetchDatasetExplorer(),
  });

  // Table state
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedScenario, setSelectedScenario] = useState('all');
  const [sortField, setSortField] = useState<'row_index' | 'amount_btc' | 'computed_risk_score'>('row_index');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  // Tab State
  const [activeTab, setActiveTab] = useState<'transactions' | 'features'>('transactions');

  // Filtered and Sorted Transactions
  const processedTransactions = useMemo(() => {
    if (!explorerData?.transactions) return [];

    let txs = [...explorerData.transactions];

    // Search filter
    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase();
      txs = txs.filter(
        (t) =>
          t.transaction_id.toLowerCase().includes(term) ||
          t.input_address.toLowerCase().includes(term) ||
          t.output_address.toLowerCase().includes(term)
      );
    }

    // Scenario filter
    if (selectedScenario !== 'all') {
      txs = txs.filter((t) => t.ground_truth_scenario === selectedScenario);
    }

    // Sort
    txs.sort((a, b) => {
      let valA = a[sortField];
      let valB = b[sortField];
      if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
      if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

    return txs;
  }, [explorerData?.transactions, searchTerm, selectedScenario, sortField, sortOrder]);

  // Paginated Results
  const totalPages = Math.max(1, Math.ceil(processedTransactions.length / pageSize));
  const paginatedTransactions = useMemo(() => {
    const start = (currentPage - 1) * pageSize;
    return processedTransactions.slice(start, start + pageSize);
  }, [processedTransactions, currentPage, pageSize]);

  const handleSort = (field: 'row_index' | 'amount_btc' | 'computed_risk_score') => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  if (isLoading) {
    return (
      <div className="h-[600px] flex items-center justify-center bg-slate-950 rounded-xl border border-slate-800">
        <div className="text-center space-y-3">
          <Loader2 className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
          <p className="text-xs text-slate-400 font-mono">Loading dataset explorer statistics & feature vectors...</p>
        </div>
      </div>
    );
  }

  if (isError || !explorerData) {
    return (
      <div className="p-8 bg-slate-900/60 rounded-xl border border-slate-800 text-center space-y-3">
        <AlertTriangle className="w-8 h-8 text-rose-400 mx-auto" />
        <h2 className="text-sm font-bold text-slate-200 uppercase font-mono">Dataset Explorer Unavailable</h2>
        <p className="text-xs text-slate-400">Failed to calculate dataset metrics. Ensure dataset pipeline is active.</p>
      </div>
    );
  }

  const { summary, scenario_distribution, extracted_features } = explorerData;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 text-[10px] font-mono uppercase font-bold rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              DATA SOURCE: {explorerData.data_source_type.toUpperCase()} DATASET
            </span>
            <span className="text-xs text-slate-400 font-mono">{explorerData.filename}</span>
          </div>
          <h1 className="text-xl font-mono font-bold text-slate-100 mt-1 flex items-center gap-2">
            <Database className="w-5 h-5 text-cyan-400" />
            <span>Dataset Explorer & Feature Inspector</span>
          </h1>
        </div>

        <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
          <span>Active Dataset ID:</span>
          <span className="px-2.5 py-1 bg-slate-950 text-cyan-300 border border-slate-800 rounded font-bold">
            {explorerData.dataset_id}
          </span>
        </div>
      </div>

      {/* DATASET SUMMARY CARDS GRID */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3 font-mono">
        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
          <span className="text-[10px] text-slate-500 block uppercase font-semibold">Total Transactions</span>
          <span className="text-lg font-bold text-slate-100">{summary.total_transactions}</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
          <span className="text-[10px] text-slate-500 block uppercase font-semibold">Unique Addresses</span>
          <span className="text-lg font-bold text-cyan-400">{summary.unique_addresses}</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
          <span className="text-[10px] text-slate-500 block uppercase font-semibold">Total Volume</span>
          <span className="text-lg font-bold text-emerald-400">{summary.total_volume_btc.toFixed(2)} BTC</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
          <span className="text-[10px] text-slate-500 block uppercase font-semibold">Avg Tx Amount</span>
          <span className="text-lg font-bold text-purple-400">{summary.avg_transaction_amount_btc.toFixed(3)} BTC</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
          <span className="text-[10px] text-slate-500 block uppercase font-semibold">Missing Values</span>
          <span className="text-lg font-bold text-amber-400">{summary.missing_values_count}</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl">
          <span className="text-[10px] text-slate-500 block uppercase font-semibold">Duplicate Records</span>
          <span className="text-lg font-bold text-slate-300">{summary.duplicate_records_count}</span>
        </div>

        <div className="p-4 bg-slate-900/60 border border-slate-800 rounded-xl col-span-2 sm:col-span-1">
          <span className="text-[10px] text-slate-500 block uppercase font-semibold">Time Span</span>
          <span className="text-xs font-bold text-slate-300 truncate block">
            {summary.time_range_start ? summary.time_range_start.substring(0, 10) : '2026-08-30'}
          </span>
        </div>
      </div>

      {/* SCENARIO DISTRIBUTION BREAKDOWN */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
          <Layers className="w-4 h-4 text-purple-400" />
          <span>Ground-Truth Scenario Distribution (Live Calculated)</span>
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 font-mono text-xs">
          {Object.entries(scenario_distribution).map(([sc, count]) => {
            const pct = ((count / Math.max(1, summary.total_transactions)) * 100).toFixed(1);
            return (
              <div key={sc} className="p-3 bg-slate-950 border border-slate-800 rounded-lg space-y-1">
                <div className="flex justify-between items-center text-[10px] text-slate-400 uppercase font-semibold">
                  <span className="truncate">{sc.replace('_', ' ')}</span>
                  <span className="text-cyan-400">{pct}%</span>
                </div>
                <div className="text-base font-bold text-slate-100">{count} records</div>
                <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                  <div className="h-full bg-cyan-400" style={{ width: `${pct}%` }}></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* TAB NAVIGATION */}
      <div className="flex border-b border-slate-800 space-x-6 text-xs font-mono font-bold uppercase">
        <button
          onClick={() => setActiveTab('transactions')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-colors ${
            activeTab === 'transactions' ? 'border-cyan-400 text-cyan-400' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Table className="w-4 h-4" />
          <span>Transaction Dataset Table ({processedTransactions.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('features')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition-colors ${
            activeTab === 'features' ? 'border-purple-400 text-purple-400' : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Cpu className="w-4 h-4" />
          <span>Extracted Entity Features ({extracted_features.length})</span>
        </button>
      </div>

      {/* TAB 1: TRANSACTION TABLE */}
      {activeTab === 'transactions' && (
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
          {/* Controls Bar: Search, Scenario Filter, Sort */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 font-mono text-xs">
            {/* Search Input */}
            <div className="relative w-full sm:w-72">
              <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Search TxID or Address..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value);
                  setCurrentPage(1);
                }}
                className="w-full pl-9 pr-3 py-2 bg-slate-950 text-slate-200 border border-slate-800 rounded-lg focus:outline-none focus:border-cyan-500"
              />
            </div>

            <div className="flex items-center space-x-3 w-full sm:w-auto">
              {/* Scenario Filter */}
              <div className="flex items-center space-x-1">
                <Filter className="w-3.5 h-3.5 text-slate-400" />
                <select
                  value={selectedScenario}
                  onChange={(e) => {
                    setSelectedScenario(e.target.value);
                    setCurrentPage(1);
                  }}
                  className="px-2.5 py-2 bg-slate-950 text-cyan-400 border border-slate-800 rounded-lg focus:outline-none"
                >
                  <option value="all">All Scenarios</option>
                  <option value="normal">Normal</option>
                  <option value="rapid_forwarding">Rapid Forwarding</option>
                  <option value="fan_out">Fan-Out</option>
                  <option value="fan_in">Fan-In</option>
                  <option value="peeling_chain">Peeling Chain</option>
                  <option value="circular_flow">Circular Flow</option>
                  <option value="dormancy_burst">Dormancy Burst</option>
                  <option value="structuring">Structuring</option>
                  <option value="risky_neighbor">Risky Neighbor</option>
                </select>
              </div>

              {/* Page Size */}
              <select
                value={pageSize}
                onChange={(e) => {
                  setPageSize(Number(e.target.value));
                  setCurrentPage(1);
                }}
                className="px-2.5 py-2 bg-slate-950 text-slate-300 border border-slate-800 rounded-lg focus:outline-none"
              >
                <option value={10}>10 / Page</option>
                <option value={25}>25 / Page</option>
                <option value={50}>50 / Page</option>
              </select>
            </div>
          </div>

          {/* Transactions Data Table */}
          <div className="overflow-x-auto border border-slate-800 rounded-xl">
            <table className="w-full text-left border-collapse font-mono text-xs">
              <thead>
                <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 text-[10px] uppercase">
                  <th className="p-3 cursor-pointer" onClick={() => handleSort('row_index')}>
                    <div className="flex items-center space-x-1">
                      <span>#</span>
                      <ArrowUpDown className="w-3 h-3" />
                    </div>
                  </th>
                  <th className="p-3">TxID</th>
                  <th className="p-3">Input Address</th>
                  <th className="p-3">Output Address</th>
                  <th className="p-3 cursor-pointer" onClick={() => handleSort('amount_btc')}>
                    <div className="flex items-center space-x-1">
                      <span>Amount (BTC)</span>
                      <ArrowUpDown className="w-3 h-3" />
                    </div>
                  </th>
                  <th className="p-3">Scenario</th>
                  <th className="p-3 cursor-pointer" onClick={() => handleSort('computed_risk_score')}>
                    <div className="flex items-center space-x-1">
                      <span>Risk Score</span>
                      <ArrowUpDown className="w-3 h-3" />
                    </div>
                  </th>
                  <th className="p-3">Top Signal</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 bg-slate-950/40">
                {paginatedTransactions.map((tx) => (
                  <tr key={tx.row_index} className="hover:bg-slate-900/60 transition-colors">
                    <td className="p-3 text-slate-500">{tx.row_index}</td>
                    <td className="p-3 font-bold text-slate-200">{tx.transaction_id.substring(0, 14)}...</td>
                    <td className="p-3 text-slate-400">{tx.input_address.substring(0, 12)}...</td>
                    <td className="p-3 text-slate-400">{tx.output_address.substring(0, 12)}...</td>
                    <td className="p-3 font-bold text-cyan-400">{tx.amount_btc.toFixed(4)} BTC</td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 text-[10px] uppercase font-bold rounded border ${
                        tx.ground_truth_scenario === 'normal' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' :
                        'bg-amber-500/10 text-amber-300 border-amber-500/30'
                      }`}>
                        {tx.ground_truth_scenario.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="p-3">
                      <span className={`font-bold ${
                        tx.computed_risk_level === 'critical' ? 'text-purple-400' :
                        tx.computed_risk_level === 'high' ? 'text-rose-400' :
                        tx.computed_risk_level === 'medium' ? 'text-amber-400' :
                        'text-emerald-400'
                      }`}>
                        {tx.computed_risk_score}/100 ({tx.computed_risk_level.toUpperCase()})
                      </span>
                    </td>
                    <td className="p-3 text-slate-300">{tx.top_signal}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination Controls */}
          <div className="flex items-center justify-between font-mono text-xs pt-2">
            <span className="text-slate-400">
              Showing Page {currentPage} of {totalPages} ({processedTransactions.length} records)
            </span>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="p-1.5 bg-slate-950 border border-slate-800 rounded disabled:opacity-40 text-slate-300"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                disabled={currentPage === totalPages}
                className="p-1.5 bg-slate-950 border border-slate-800 rounded disabled:opacity-40 text-slate-300"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: EXTRACTED FEATURES TABLE */}
      {activeTab === 'features' && (
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center space-x-2">
            <Cpu className="w-4 h-4 text-purple-400" />
            <span>Extracted Entity Numeric Feature Vectors (Calculated from Dataset Graph)</span>
          </h3>

          <div className="overflow-x-auto border border-slate-800 rounded-xl">
            <table className="w-full text-left border-collapse font-mono text-xs">
              <thead>
                <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 text-[10px] uppercase">
                  <th className="p-3">Entity Address</th>
                  <th className="p-3">Vol (BTC)</th>
                  <th className="p-3">In-Deg</th>
                  <th className="p-3">Out-Deg</th>
                  <th className="p-3">PageRank</th>
                  <th className="p-3">Peel Steps</th>
                  <th className="p-3">Dormant Days</th>
                  <th className="p-3">Micro Tx</th>
                  <th className="p-3">Hop Dist</th>
                  <th className="p-3">Cycle?</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 bg-slate-950/40">
                {extracted_features.map((feat, i) => (
                  <tr key={i} className="hover:bg-slate-900/60 transition-colors">
                    <td className="p-3 font-bold text-slate-200">{feat.address.substring(0, 16)}...</td>
                    <td className="p-3 font-bold text-cyan-400">{feat.amount_btc.toFixed(3)} BTC</td>
                    <td className="p-3 text-slate-300">{feat.in_degree}</td>
                    <td className="p-3 text-slate-300">{feat.out_degree}</td>
                    <td className="p-3 text-purple-400 font-bold">{feat.pagerank}</td>
                    <td className="p-3 text-slate-400">{feat.peel_steps}</td>
                    <td className="p-3 text-slate-400">{feat.dormant_days}d</td>
                    <td className="p-3 text-slate-400">{feat.micro_tx_count}</td>
                    <td className="p-3 text-slate-400">{feat.hop_distance}</td>
                    <td className="p-3">
                      {feat.has_cycle ? (
                        <span className="px-2 py-0.5 text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/30 rounded uppercase font-bold">
                          Yes
                        </span>
                      ) : (
                        <span className="text-slate-500">No</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
