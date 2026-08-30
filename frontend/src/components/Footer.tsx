import React from 'react';
import { AlertCircle, Lock } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-auto bg-[#070a12] border-t border-slate-800/80 py-6 text-xs text-slate-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-4">
        {/* Responsible AI Disclaimer Banner */}
        <div className="bg-amber-500/5 border border-amber-500/20 rounded-lg p-3 flex items-start space-x-3 text-amber-200/90">
          <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="font-semibold text-amber-400 text-[11px] uppercase tracking-wide">
              Responsible AI & Legal Disclaimer
            </p>
            <p className="text-[11px] leading-relaxed text-slate-300">
              ChainSentinel risk scores (0-100) and behavioral indicators are transparent prioritization signals for forensic triage. 
              They <strong>do not identify individual persons</strong> or constitute <strong>legal proof of criminal guilt</strong>. 
              All analysis requires qualified human investigator review.
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between pt-2 border-t border-slate-800/50 text-[11px]">
          <div className="flex items-center space-x-2 text-slate-400">
            <Lock className="w-3.5 h-3.5 text-emerald-400" />
            <span>Read-Only Platform — Zero Wallet/Key Access</span>
          </div>

          <div className="mt-2 sm:mt-0 font-mono text-slate-400">
            ChainSentinel v0.1.0 • Smart India Hackathon 2026 (SIH26146)
          </div>
        </div>
      </div>
    </footer>
  );
};
