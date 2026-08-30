import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Briefcase,
  PlusCircle,
  FileText,
  Clock,
  User,
  Shield,
  Loader2,
  X,
  MessageSquare,
  History,
  ExternalLink,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import {
  fetchCases,
  createCase,
  addCaseNote,
  getCasePdfUrl,
  CaseItem
} from '../services/api';
import { useAuth } from '../context/AuthContext';

export const CasesPage: React.FC = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');

  const [isCreateModalOpen, setIsCreateModalOpen] = useState<boolean>(false);
  const [expandedCaseId, setExpandedCaseId] = useState<string | null>('case-001');

  // Form states for creating case
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newPriority, setNewPriority] = useState('medium');
  const [newAddress, setNewAddress] = useState('');

  // Form states for adding note
  const [noteTextMap, setNoteTextMap] = useState<Record<string, string>>({});

  const { data: cases, isLoading, isError } = useQuery({
    queryKey: ['cases', statusFilter, priorityFilter],
    queryFn: () => fetchCases(statusFilter, priorityFilter),
  });

  const createCaseMutation = useMutation({
    mutationFn: createCase,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cases'] });
      queryClient.invalidateQueries({ queryKey: ['dashboardSummary'] });
      setIsCreateModalOpen(false);
      setNewTitle('');
      setNewDescription('');
      setNewAddress('');
    },
  });

  const addNoteMutation = useMutation({
    mutationFn: ({ caseId, text }: { caseId: string; text: string }) =>
      addCaseNote(caseId, text, user?.full_name || 'Lead Investigator'),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['cases'] });
      setNoteTextMap((prev) => ({ ...prev, [variables.caseId]: '' }));
    },
  });

  const handleCreateCaseSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newDescription.trim()) return;

    createCaseMutation.mutate({
      title: newTitle.trim(),
      description: newDescription.trim(),
      priority: newPriority as any,
      status: 'open',
      assigned_investigator: user?.full_name || 'Lead Investigator',
      linked_addresses: newAddress.trim() ? [newAddress.trim()] : [],
    });
  };

  const handleAddNoteSubmit = (caseId: string, e: React.FormEvent) => {
    e.preventDefault();
    const text = noteTextMap[caseId];
    if (!text || !text.trim()) return;
    addNoteMutation.mutate({ caseId, text: text.trim() });
  };

  const handleExportPdf = (caseId: string) => {
    const pdfUrl = getCasePdfUrl(caseId);
    window.open(pdfUrl, '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-slate-900/60 p-6 rounded-xl border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center space-x-2">
            <Briefcase className="w-5 h-5 text-cyan-400" />
            <span>Investigative Case Management & Audit Trail</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Organize flagged transactions, log analyst notes, maintain audit trails, and export court-ready PDF reports.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs font-bold rounded-lg flex items-center space-x-2"
          >
            <PlusCircle className="w-4 h-4" />
            <span>New Investigation Case</span>
          </button>
        </div>
      </div>

      {/* Cases List & Details Accordion */}
      {isLoading ? (
        <div className="p-12 text-center space-y-3">
          <Loader2 className="w-8 h-8 text-cyan-400 animate-spin mx-auto" />
          <p className="text-xs text-slate-400 font-mono">Loading Investigative Cases...</p>
        </div>
      ) : isError ? (
        <div className="p-8 text-center text-xs text-rose-400">Failed to load cases repository.</div>
      ) : (
        <div className="space-y-4">
          {cases?.map((item) => {
            const isExpanded = expandedCaseId === item.id;
            return (
              <div key={item.id} className="bg-slate-900/60 rounded-xl border border-slate-800 overflow-hidden transition-all">
                {/* Case Row Header */}
                <div
                  onClick={() => setExpandedCaseId(isExpanded ? null : item.id)}
                  className="p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer hover:bg-slate-800/30 transition-colors"
                >
                  <div className="space-y-1">
                    <div className="flex items-center space-x-3">
                      <span className="font-mono text-xs font-bold text-cyan-400">{item.case_number}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase border ${
                        item.priority === 'critical' ? 'bg-purple-500/10 text-purple-400 border-purple-500/30' :
                        item.priority === 'high' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                        item.priority === 'medium' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
                        'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      }`}>
                        {item.priority.toUpperCase()} PRIORITY
                      </span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-slate-800 text-slate-300 border border-slate-700">
                        {item.status.replace('_', ' ').toUpperCase()}
                      </span>
                    </div>
                    <h2 className="text-sm font-bold text-slate-100">{item.title}</h2>
                  </div>

                  <div className="flex items-center space-x-4">
                    <div className="text-right text-xs font-mono text-slate-400">
                      <span className="block text-slate-300">{item.assigned_investigator}</span>
                      <span className="text-[10px]">{item.created_at.slice(0, 10)}</span>
                    </div>

                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleExportPdf(item.id);
                      }}
                      className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded border border-slate-700 flex items-center space-x-1.5 text-xs font-mono"
                    >
                      <FileText className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Export PDF</span>
                    </button>

                    {isExpanded ? <ChevronUp className="w-5 h-5 text-slate-400" /> : <ChevronDown className="w-5 h-5 text-slate-400" />}
                  </div>
                </div>

                {/* Expanded Case Details Body */}
                {isExpanded && (
                  <div className="p-6 border-t border-slate-800/80 bg-slate-950/60 space-y-6">
                    <div className="space-y-2">
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Case Description</h3>
                      <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-4 rounded-lg border border-slate-800">
                        {item.description}
                      </p>
                    </div>

                    {/* Linked Entities */}
                    <div className="space-y-2">
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Linked Forensic Entities</h3>
                      <div className="flex flex-wrap gap-2">
                        {item.linked_addresses.map((addr, idx) => (
                          <span key={idx} className="px-3 py-1 bg-slate-900 border border-slate-800 text-cyan-400 text-xs font-mono rounded">
                            Address: {addr}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Notes History */}
                    <div className="space-y-3">
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <MessageSquare className="w-4 h-4 text-cyan-400" />
                        <span>Analyst Investigative Notes ({item.notes?.length || 0})</span>
                      </h3>

                      <div className="space-y-2">
                        {item.notes?.map((note) => (
                          <div key={note.id} className="p-3 bg-slate-900 border border-slate-800 rounded-lg text-xs space-y-1">
                            <div className="flex justify-between font-mono text-[10px] text-slate-400">
                              <span className="font-bold text-slate-300">{note.author_name}</span>
                              <span>{note.created_at.slice(0, 16).replace('T', ' ')}</span>
                            </div>
                            <p className="text-slate-300 leading-relaxed">{note.note_text}</p>
                          </div>
                        ))}
                      </div>

                      {/* Add Note Input Form */}
                      <form onSubmit={(e) => handleAddNoteSubmit(item.id, e)} className="flex gap-2">
                        <input
                          type="text"
                          placeholder="Log an investigative note..."
                          value={noteTextMap[item.id] || ''}
                          onChange={(e) => setNoteTextMap({ ...noteTextMap, [item.id]: e.target.value })}
                          className="flex-1 px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-200 focus:outline-none focus:border-cyan-500"
                        />
                        <button
                          type="submit"
                          disabled={addNoteMutation.isPending}
                          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-400 text-xs font-bold rounded-lg border border-slate-700"
                        >
                          Add Note
                        </button>
                      </form>
                    </div>

                    {/* Audit Log Activity */}
                    <div className="space-y-2 pt-4 border-t border-slate-800">
                      <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                        <History className="w-4 h-4 text-purple-400" />
                        <span>Audit Trail Log</span>
                      </h3>
                      <div className="space-y-1 font-mono text-[11px] text-slate-400">
                        {item.audit_logs?.map((audit) => (
                          <div key={audit.id} className="flex justify-between py-1 border-b border-slate-800/40">
                            <span><b>{audit.action}</b> by {audit.actor_id}</span>
                            <span className="text-[10px] text-slate-500">{audit.created_at.slice(0, 16).replace('T', ' ')}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* New Case Creation Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 max-w-lg w-full space-y-4 shadow-2xl">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-cyan-400" />
                <span>Create New Investigation Case</span>
              </h2>
              <button onClick={() => setIsCreateModalOpen(false)} className="text-slate-400 hover:text-slate-200">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleCreateCaseSubmit} className="space-y-4 text-xs font-mono">
              <div className="space-y-1">
                <label className="text-slate-400">Case Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g., Ransomware Cluster Triage"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="space-y-1">
                <label className="text-slate-400">Description</label>
                <textarea
                  required
                  rows={3}
                  placeholder="Detailed investigative rationale and scope..."
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1">
                  <label className="text-slate-400">Priority</label>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-slate-400">Primary Linked Address</label>
                  <input
                    type="text"
                    placeholder="bc1q..."
                    value={newAddress}
                    onChange={(e) => setNewAddress(e.target.value)}
                    className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-lg text-slate-200 focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={createCaseMutation.isPending}
                  className="px-5 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-lg flex items-center space-x-2"
                >
                  {createCaseMutation.isPending && <Loader2 className="w-4 h-4 animate-spin" />}
                  <span>Create Case</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
