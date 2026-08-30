import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Shield, Cpu, Network, Lock, BarChart3, CheckCircle2, AlertTriangle, Info } from 'lucide-react';
import { fetchMlModelInfo } from '../services/api';

export const AboutPage: React.FC = () => {
  const { data: mlInfo, isLoading } = useQuery({
    queryKey: ['mlModelInfo'],
    queryFn: fetchMlModelInfo,
  });

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Overview Banner */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-3">
        <div className="flex items-center space-x-3">
          <Shield className="w-6 h-6 text-cyan-400" />
          <h1 className="text-xl font-bold text-slate-100">ChainSentinel Architecture & Responsible AI Methodology</h1>
        </div>
        <p className="text-xs text-slate-400 leading-relaxed">
          ChainSentinel is built specifically for Smart India Hackathon 2026 (SIH26146) to provide transparent, explainable, and responsible Bitcoin transaction traffic analysis for law enforcement and financial intelligence analysts.
        </p>
      </div>

      {/* Sub-Engine Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900/60 p-5 rounded-xl border border-slate-800 space-y-3">
          <Cpu className="w-5 h-5 text-cyan-400" />
          <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider">1. Rule Engine (0-40 Pts)</h2>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Detects 10 deterministic behavioral patterns: peeling chain, fan-out, fan-in, rapid forwarding, circular flow, dormancy burst, structuring, and risky-neighbor distance.
          </p>
        </div>

        <div className="bg-slate-900/60 p-5 rounded-xl border border-slate-800 space-y-3">
          <Cpu className="w-5 h-5 text-purple-400" />
          <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider">2. ML Baseline (0-35 Pts)</h2>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Supervised RandomForest risk probability combined with IsolationForest anomaly scoring for unlabelled transaction volume/frequency spikes.
          </p>
        </div>

        <div className="bg-slate-900/60 p-5 rounded-xl border border-slate-800 space-y-3">
          <Network className="w-5 h-5 text-amber-400" />
          <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider">3. Graph Centrality (0-25 Pts)</h2>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            NetworkX graph topological analysis including PageRank, in/out degree ratios, shortest path to flagged demo clusters, and cycle detection.
          </p>
        </div>
      </div>

      {/* MODEL INFORMATION SECTION */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-purple-400" />
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-200">MODEL INFORMATION</h2>
          </div>
          <span className="px-2 py-0.5 bg-purple-500/10 text-purple-400 border border-purple-500/30 text-[10px] font-mono rounded font-bold">
            v1.0.0 (Scikit-Learn Baseline)
          </span>
        </div>

        {/* Model Declarations Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
            <span className="text-[10px] font-mono text-cyan-400 font-bold uppercase block">Supervised Model</span>
            <h3 className="text-sm font-mono font-bold text-slate-100">Model: RandomForest</h3>
            <p className="text-xs text-slate-300"><strong>Purpose:</strong> Behavioral risk prioritization</p>
            <p className="text-[11px] text-slate-400"><strong>Parameters:</strong> n_estimators=100, max_depth=6, random_state=42</p>
          </div>

          <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
            <span className="text-[10px] font-mono text-purple-400 font-bold uppercase block">Unsupervised Anomaly Model</span>
            <h3 className="text-sm font-mono font-bold text-slate-100">Second model: IsolationForest</h3>
            <p className="text-xs text-slate-300"><strong>Purpose:</strong> Unsupervised anomaly detection</p>
            <p className="text-[11px] text-slate-400"><strong>Parameters:</strong> n_estimators=100, contamination=0.3, random_state=42</p>
          </div>
        </div>

        {/* Feature Importance Section */}
        {mlInfo?.feature_importances && (
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              RandomForest Feature Importances (feature_importances_)
            </h3>
            <div className="space-y-2 bg-slate-950 p-4 rounded-xl border border-slate-800">
              {Object.entries(mlInfo.feature_importances)
                .sort((a, b) => b[1] - a[1])
                .map(([feat, val]) => (
                  <div key={feat} className="space-y-1 text-xs">
                    <div className="flex justify-between font-mono">
                      <span className="text-slate-400">{feat}</span>
                      <span className="text-cyan-400 font-bold">{(val * 100).toFixed(2)}%</span>
                    </div>
                    <div className="h-1.5 bg-slate-900 rounded-full overflow-hidden">
                      <div className="h-full bg-cyan-400" style={{ width: `${val * 100}%` }}></div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Held-Out Evaluation Metrics Grid */}
        {mlInfo?.held_out_metrics && (
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              Held-Out Test Set Evaluation Metrics (20% Stratified Holdout)
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono">
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-center">
                <span className="text-[10px] text-slate-400 block uppercase font-semibold">Precision</span>
                <span className="text-base font-bold text-emerald-400">{(mlInfo.held_out_metrics.precision * 100).toFixed(1)}%</span>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-center">
                <span className="text-[10px] text-slate-400 block uppercase font-semibold">Recall</span>
                <span className="text-base font-bold text-emerald-400">{(mlInfo.held_out_metrics.recall * 100).toFixed(1)}%</span>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-center">
                <span className="text-[10px] text-slate-400 block uppercase font-semibold">F1 Score</span>
                <span className="text-base font-bold text-cyan-400">{(mlInfo.held_out_metrics.f1_score * 100).toFixed(1)}%</span>
              </div>
              <div className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-center">
                <span className="text-[10px] text-slate-400 block uppercase font-semibold">ROC-AUC</span>
                <span className="text-base font-bold text-purple-400">{(mlInfo.held_out_metrics.roc_auc * 100).toFixed(1)}%</span>
              </div>
            </div>

            {/* Confusion Matrix Display */}
            {mlInfo.held_out_metrics.confusion_matrix && (
              <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2">
                <span className="text-xs font-bold text-slate-300 block uppercase tracking-wider">
                  Held-Out Confusion Matrix ({mlInfo.held_out_metrics.test_samples} Test Samples)
                </span>
                <div className="grid grid-cols-2 gap-3 font-mono text-xs text-center">
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">True Negatives (TN)</span>
                    <span className="text-slate-200 font-bold text-sm">{mlInfo.held_out_metrics.confusion_matrix.tn}</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">False Positives (FP)</span>
                    <span className="text-amber-400 font-bold text-sm">{mlInfo.held_out_metrics.confusion_matrix.fp}</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">False Negatives (FN)</span>
                    <span className="text-rose-400 font-bold text-sm">{mlInfo.held_out_metrics.confusion_matrix.fn}</span>
                  </div>
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded">
                    <span className="text-slate-500 text-[10px] block uppercase">True Positives (TP)</span>
                    <span className="text-emerald-400 font-bold text-sm">{mlInfo.held_out_metrics.confusion_matrix.tp}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="p-3 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-300 text-xs flex items-center space-x-2">
          <Info className="w-4 h-4 flex-shrink-0" />
          <span>
            {mlInfo?.disclaimer || "Machine-learning outputs are advisory prioritization signals, NOT proof of criminal activity."}
          </span>
        </div>
      </div>

      {/* Ethical & Privacy Guardrails Card */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 space-y-3">
        <div className="flex items-center space-x-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
          <Lock className="w-4 h-4" />
          <span>Ethical & Privacy Guardrails</span>
        </div>
        <ul className="list-disc list-inside text-xs text-slate-400 space-y-1.5 leading-relaxed">
          <li>ChainSentinel operates strictly in read-only mode and never requests private keys or wallet credentials.</li>
          <li>Risk scores are prioritization indicators to organize human investigation workflows and carry no legal proof of criminality.</li>
          <li>System functions completely offline with deterministic demo data for judging reliability.</li>
        </ul>
      </div>
    </div>
  );
};
