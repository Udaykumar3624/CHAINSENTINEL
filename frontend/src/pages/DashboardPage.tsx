import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import {
  Activity,
  AlertTriangle,
  ShieldAlert,
  Network,
  ArrowUpRight,
  PlayCircle,
  Clock,
  ExternalLink,
  Loader2,
  Database,
  RotateCcw,
  Sparkles,
  FileSpreadsheet
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts';
import { fetchDashboardSummary, fetchDemoScenarios, resetActiveDataset, loadDemoDataset } from '../services/api';

const RISK_COLORS = {
  low: '#10b981',
  medium: '#f59e0b',
  high: '#ef4444',
  critical: '#a855f7',
};

export const DashboardPage: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: summary, isLoading: isSummaryLoading, isError: isSummaryError } = useQuery({
    queryKey: ['dashboardSummary'],
    queryFn: fetchDashboardSummary,
  });

  const { data: demoScenarios } = useQuery({
    queryKey: ['demoScenarios'],
    queryFn: fetchDemoScenarios,
  });

  const resetMutation = useMutation({
    mutationFn: resetActiveDataset,
    onSuccess: (data) => {
      queryClient.setQueryData(['dashboardSummary'], data);
    },
  });

  const loadDemoMutation = useMutation({
    mutationFn: loadDemoDataset,
    onSuccess: (data) => {
      queryClient.setQueryData(['dashboardSummary'], data);
    },
  });

  const activeInfo = summary?.active_dataset;

  const pieData = summary
    ? [
        { name: 'Low (0-29)', value: summary.risk_distribution.low, color: RISK_COLORS.low },
        { name: 'Medium (30-69)', value: summary.risk_distribution.medium, color: RISK_COLORS.medium },
        { name: 'High (70-89)', value: summary.risk_distribution.high, color: RISK_COLORS.high },
        { name: 'Critical (90-100)', value: summary.risk_distribution.critical, color: RISK_COLORS.critical },
      ]
    : [];

  const kpis = [
    {
      title: 'Transactions Analyzed',
      value: summary ? summary.kpis.total_transactions_analyzed.toLocaleString() : '0',
      change: activeInfo ? `${activeInfo.row_count} rows` : '0 rows',
      icon: Activity,
      color: 'text-cyan-400',
      bg: 'bg-cyan-500/10 border-cyan-500/20'
    },
    {
      title: 'High & Critical Alerts',
      value: summary ? summary.kpis.high_critical_alerts.toString() : '0',
      change: 'Calculated live',
      icon: ShieldAlert,
      color: 'text-rose-400',
      bg: 'bg-rose-500/10 border-rose-500/20'
    },
    {
      title: 'Active Cases',
      value: summary ? summary.kpis.open_cases.toString() : '0',
      change: '1 in triage',
      icon: AlertTriangle,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10 border-amber-500/20'
    },
    {
      title: 'Flagged Clusters',
      value: summary ? summary.kpis.flagged_clusters.toString() : '0',
      change: 'NetworkX graph',
      icon: Network,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10 border-purple-500/20'
    },
  ];

  if (isSummaryLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <Loader2 className="w-8 h-8 text-cyan-400 animate-spin" />
        <p className="text-xs text-slate-400 font-mono">Loading Data-Driven ChainSentinel Dashboard...</p>
      </div>
    );
  }

  if (isSummaryError) {
    return (
      <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-6 text-center space-y-3">
        <AlertTriangle className="w-8 h-8 text-rose-400 mx-auto" />
        <h2 className="text-sm font-bold text-rose-400">Failed to connect to ChainSentinel Backend</h2>
        <p className="text-xs text-slate-300">Ensure the ChainSentinel FastAPI backend service is operational and accessible.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-xl border border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-3">
            <span>Executive Risk Overview</span>
            <span className="text-xs font-mono font-normal px-2.5 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
              SIH26146
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Explainable AI-powered Bitcoin transaction traffic analysis for intelligence triage.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/explorer"
            className="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-cyan-300 text-xs font-mono rounded-lg transition-colors flex items-center gap-2"
          >
            <Database className="w-4 h-4 text-cyan-400" />
            <span>Dataset Explorer</span>
          </Link>
          <Link
            to="/analyze"
            className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs rounded-lg transition-colors flex items-center gap-2"
          >
            <span>Start Analysis</span>
            <ArrowUpRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* ACTIVE DATASET PROVENANCE & CONTROLS BANNER */}
      <div className="bg-slate-900/80 p-5 rounded-xl border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3 font-mono">
          <div className="flex items-center space-x-3">
            <span className="px-2.5 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 text-xs font-bold uppercase rounded flex items-center gap-1.5">
              <FileSpreadsheet className="w-4 h-4" />
              {activeInfo?.data_source_label || "DATA SOURCE: DEMO DATASET"}
            </span>
            <span className="text-xs text-slate-300">
              Active File: <strong className="text-cyan-400">{activeInfo?.filename || "synthetic_dataset_seed42_demo.csv"}</strong>
            </span>
          </div>

          {/* DATASET CONTROLS */}
          <div className="flex items-center space-x-2 text-xs">
            <button
              onClick={() => loadDemoMutation.mutate()}
              disabled={loadDemoMutation.isPending}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700 flex items-center gap-1.5 transition-colors disabled:opacity-50"
            >
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>Load Demo Dataset</span>
            </button>
            <button
              onClick={() => resetMutation.mutate()}
              disabled={resetMutation.isPending}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-rose-300 rounded border border-slate-700 flex items-center gap-1.5 transition-colors disabled:opacity-50"
            >
              <RotateCcw className="w-3.5 h-3.5 text-rose-400" />
              <span>Reset Dataset</span>
            </button>
            <Link
              to="/dataset"
              className="px-3 py-1.5 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 rounded border border-cyan-500/30 flex items-center gap-1.5 transition-colors font-bold"
            >
              <Database className="w-3.5 h-3.5" />
              <span>Upload / Generate</span>
            </Link>
          </div>
        </div>

        {/* METADATA STRIP */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
          <div className="p-2.5 bg-slate-950 border border-slate-800/80 rounded-lg">
            <span className="text-slate-500 text-[10px] block uppercase">Data Source Type</span>
            <span className="text-cyan-400 font-bold">{activeInfo?.data_source_type || "Synthetic"}</span>
          </div>
          <div className="p-2.5 bg-slate-950 border border-slate-800/80 rounded-lg">
            <span className="text-slate-500 text-[10px] block uppercase">Analyzed Transactions</span>
            <span className="text-slate-200 font-bold">{activeInfo?.row_count ?? 100} Rows</span>
          </div>
          <div className="p-2.5 bg-slate-950 border border-slate-800/80 rounded-lg">
            <span className="text-slate-500 text-[10px] block uppercase">Pipeline Status</span>
            <span className="text-emerald-400 font-bold">{activeInfo?.analysis_status || "Completed"}</span>
          </div>
          <div className="p-2.5 bg-slate-950 border border-slate-800/80 rounded-lg">
            <span className="text-slate-500 text-[10px] block uppercase">Loaded Timestamp</span>
            <span className="text-purple-400 font-bold truncate block">{activeInfo?.created_at ? activeInfo.created_at.substring(0, 19) : "2026-08-30"}</span>
          </div>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div
              key={idx}
              className="bg-slate-900/60 p-5 rounded-xl border border-slate-800 flex items-center justify-between hover:border-slate-700 transition-colors"
            >
              <div className="space-y-1">
                <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{kpi.title}</p>
                <p className="text-2xl font-bold text-slate-100 font-mono">{kpi.value}</p>
                <p className="text-[11px] text-slate-500 font-mono">{kpi.change}</p>
              </div>
              <div className={`p-3 rounded-xl border ${kpi.bg}`}>
                <Icon className={`w-6 h-6 ${kpi.color}`} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution Donut Chart */}
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider font-mono">
              Risk Distribution Breakdown
            </h2>
            <span className="text-[11px] font-mono text-slate-500">Calculated Live</span>
          </div>

          <div className="h-[220px] relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} stroke="#090d16" strokeWidth={2} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  itemStyle={{ color: '#f8fafc', fontSize: '12px', fontFamily: 'monospace' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Distribution Legend */}
          <div className="grid grid-cols-2 gap-2 text-xs font-mono pt-2 border-t border-slate-800">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center justify-between p-1.5 rounded bg-slate-950/40">
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-slate-300 text-[11px]">{item.name.split(' ')[0]}</span>
                </div>
                <span className="font-bold text-slate-100">{item.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* 7-Day Activity Trend Chart */}
        <div className="lg:col-span-2 bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider font-mono">
              Transaction Traffic & Risk Trend
            </h2>
            <span className="text-[11px] font-mono text-cyan-400">Timestamp Grouped</span>
          </div>

          <div className="h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={summary?.activity_trend || []}>
                <defs>
                  <linearGradient id="colorHigh" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorMed" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11, fontFamily: 'monospace' }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11, fontFamily: 'monospace' }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  itemStyle={{ fontSize: '12px', fontFamily: 'monospace' }}
                />
                <Area type="monotone" dataKey="critical_count" name="Critical" stroke="#a855f7" fillOpacity={1} fill="url(#colorHigh)" />
                <Area type="monotone" dataKey="high_count" name="High Risk" stroke="#ef4444" fillOpacity={1} fill="url(#colorHigh)" />
                <Area type="monotone" dataKey="medium_count" name="Medium Risk" stroke="#f59e0b" fillOpacity={1} fill="url(#colorMed)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 pt-2 border-t border-slate-800">
            <span>Aggregated from active dataset records.</span>
            <Link to="/explorer" className="text-cyan-400 hover:underline flex items-center gap-1">
              <span>View Full Dataset Explorer</span>
              <ExternalLink className="w-3 h-3" />
            </Link>
          </div>
        </div>
      </div>

      {/* Demo Scenario Triage Cards & Recent Alerts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Demo Scenarios Showcase */}
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
              <PlayCircle className="w-4 h-4 text-cyan-400" />
              <span>SIH Judging Scenarios</span>
            </h2>
            <span className="text-[11px] font-mono text-slate-500">Deterministic Benchmarks</span>
          </div>

          <div className="space-y-3">
            {demoScenarios?.scenarios.map((sc) => (
              <div
                key={sc.id}
                className="p-4 bg-slate-950/60 border border-slate-800 rounded-xl hover:border-slate-700 transition-colors flex items-center justify-between"
              >
                <div className="space-y-1 max-w-[75%]">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-xs text-slate-200 font-mono">{sc.title}</span>
                    <span className={`px-2 py-0.5 text-[9px] font-mono font-bold uppercase rounded border ${
                      sc.risk_level === 'critical' || sc.risk_level === 'high'
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                    }`}>
                      {sc.risk_level} ({sc.expected_score}/100)
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 line-clamp-1">{sc.description}</p>
                </div>

                <Link
                  to={`/analyze`}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 text-xs font-mono font-semibold rounded border border-slate-700 flex items-center gap-1"
                >
                  <span>Test</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Behavioral Alerts Queue */}
        <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider font-mono flex items-center gap-2">
              <ShieldAlert className="w-4 h-4 text-rose-400" />
              <span>Recent Behavioral Alerts</span>
            </h2>
            <Link to="/alerts" className="text-xs font-mono text-cyan-400 hover:underline">
              View All Queue ({summary?.recent_alerts.length || 0})
            </Link>
          </div>

          <div className="space-y-2.5">
            {summary?.recent_alerts.slice(0, 4).map((alert) => (
              <div
                key={alert.id}
                className="p-3 bg-slate-950/60 border border-slate-800/80 rounded-lg flex items-center justify-between text-xs font-mono"
              >
                <div className="space-y-1 max-w-[70%]">
                  <div className="flex items-center space-x-2">
                    <span className="text-rose-400 font-bold">{alert.alert_code}</span>
                    <span className="text-slate-400 text-[11px] truncate">{alert.subject_id}</span>
                  </div>
                  <p className="text-[11px] text-slate-300 truncate">{alert.top_signal}</p>
                </div>

                <div className="text-right space-y-1">
                  <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded border block ${
                    alert.risk_level === 'critical'
                      ? 'bg-purple-500/10 text-purple-400 border-purple-500/30'
                      : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                  }`}>
                    {alert.risk_score}/100 {alert.risk_level}
                  </span>
                  <Link
                    to={`/investigate/${alert.subject_id}`}
                    className="text-[10px] text-cyan-400 hover:underline inline-flex items-center gap-0.5"
                  >
                    <span>Investigate</span>
                    <ArrowUpRight className="w-3 h-3" />
                  </Link>
                </div>
              </div>
            ))}

            {(!summary?.recent_alerts || summary.recent_alerts.length === 0) && (
              <div className="p-6 text-center text-slate-500 font-mono text-xs border border-dashed border-slate-800 rounded-lg">
                No high-risk alerts detected in the current active dataset.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
