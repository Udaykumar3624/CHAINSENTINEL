import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import { CytoscapeNodeWrapper, CytoscapeEdgeWrapper } from '../services/api';

interface CytoscapeGraphProps {
  nodes: CytoscapeNodeWrapper[];
  edges: CytoscapeEdgeWrapper[];
  onSelectNode: (nodeData: any) => void;
  riskFilter: string;
  minAmount: number;
}

const RISK_COLORS: Record<string, string> = {
  low: '#10b981',
  medium: '#f59e0b',
  high: '#ef4444',
  critical: '#a855f7',
  unknown: '#64748b',
};

export const CytoscapeGraph: React.FC<CytoscapeGraphProps> = ({
  nodes,
  edges,
  onSelectNode,
  riskFilter,
  minAmount,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Filter elements based on UI controls
    const filteredNodes = nodes.filter((n) => {
      if (riskFilter !== 'all' && n.data.risk_level !== riskFilter) return false;
      return true;
    });

    const validNodeIds = new Set(filteredNodes.map((n) => n.data.id));

    const filteredEdges = edges.filter((e) => {
      if (!validNodeIds.has(e.data.source) || !validNodeIds.has(e.data.target)) return false;
      if (minAmount > 0 && e.data.amount < minAmount) return false;
      return true;
    });

    const cyElements = [
      ...filteredNodes.map((n) => ({ data: n.data })),
      ...filteredEdges.map((e) => ({ data: e.data })),
    ];

    const cy = cytoscape({
      container: containerRef.current,
      elements: cyElements,
      style: [
        {
          selector: 'node',
          style: {
            label: 'data(label)',
            'color': '#f8fafc',
            'font-size': '10px',
            'font-family': 'JetBrains Mono, monospace',
            'text-valign': 'bottom',
            'text-margin-y': 4,
            'background-color': (ele: any) => RISK_COLORS[ele.data('risk_level')] || '#64748b',
            'border-width': 2,
            'border-color': '#0f172a',
            'width': (ele: any) => (ele.data('risk_score') ? 24 + ele.data('risk_score') * 0.2 : 28),
            'height': (ele: any) => (ele.data('risk_score') ? 24 + ele.data('risk_score') * 0.2 : 28),
          },
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 4,
            'border-color': '#38bdf8',
          },
        },
        {
          selector: 'edge',
          style: {
            'width': (ele: any) => Math.max(1.5, Math.min(6, (ele.data('amount') || 1) * 0.3)),
            'line-color': (ele: any) => RISK_COLORS[ele.data('risk_level')] || '#334155',
            'target-arrow-color': (ele: any) => RISK_COLORS[ele.data('risk_level')] || '#334155',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'opacity': 0.8,
            'label': (ele: any) => `${ele.data('amount')} BTC`,
            'font-size': '8px',
            'color': '#94a3b8',
            'text-rotation': 'autorotate',
          },
        },
      ],
      layout: {
        name: 'breadthfirst',
        directed: true,
        padding: 40,
        spacingFactor: 1.25,
      },
    });

    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      onSelectNode(node.data());
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [nodes, edges, riskFilter, minAmount]);

  return (
    <div className="w-full h-full relative">
      <div ref={containerRef} className="w-full h-full min-h-[380px] bg-slate-950 rounded-lg" />
    </div>
  );
};
