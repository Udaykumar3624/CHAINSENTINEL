import os
import io
import csv
import networkx as nx
from typing import Dict, Any, List, Set, Tuple, Optional
from app.schemas.graph import (
    GraphResponse, CytoscapeNodeWrapper, CytoscapeNodeData,
    CytoscapeEdgeWrapper, CytoscapeEdgeData, GraphMetricsSummary, GraphNodeMetadata
)
from app.core.config import settings
from app.core.security import RESPONSIBLE_AI_DISCLAIMER
from app.services.analysis.analysis_service import AnalysisService

FLAGGED_DEMO_ENTITIES = {
    "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0": "DEMO_RANSOMWARE_PAYOUT_01",
    "bc1qcycle000111222333444555666777888999": "DEMO_WASH_CLUSTER_02",
    "bc1qfanout9876543210split9876543210abc": "DEMO_MIXER_INPUT_03"
}

DATASETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "datasets_store"))

class GraphService:
    def __init__(self, max_nodes: int = None):
        self.max_nodes = max_nodes or settings.MAX_GRAPH_NODES
        self.analysis_service = AnalysisService()

    def build_graph(
        self,
        subject_type: str,
        subject_id: str,
        hops: int = 1,
        risk_filter: str = "all",
        dataset_id: Optional[str] = None
    ) -> GraphResponse:
        # Check if dataset file exists
        dataset_filepath = self._find_dataset_file(dataset_id, subject_id)
        if dataset_filepath and os.path.exists(dataset_filepath):
            return self._build_from_dataset_file(dataset_filepath, subject_type, subject_id, hops, risk_filter)
        else:
            return self.build_demo_graph(subject_type, subject_id, hops, risk_filter)

    def _find_dataset_file(self, dataset_id: Optional[str], subject_id: str) -> Optional[str]:
        if not os.path.exists(DATASETS_DIR):
            return None
        for fname in os.listdir(DATASETS_DIR):
            if fname.endswith(".csv"):
                if dataset_id and dataset_id in fname:
                    return os.path.join(DATASETS_DIR, fname)
                if subject_id and subject_id in fname:
                    return os.path.join(DATASETS_DIR, fname)
        # Fallback to newest generated CSV in DATASETS_DIR if any
        csv_files = [os.path.join(DATASETS_DIR, f) for f in os.listdir(DATASETS_DIR) if f.endswith(".csv")]
        if csv_files:
            csv_files.sort(key=os.path.getmtime, reverse=True)
            return csv_files[0]
        return None

    def _build_from_dataset_file(
        self,
        filepath: str,
        subject_type: str,
        subject_id: str,
        hops: int,
        risk_filter: str
    ) -> GraphResponse:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))

        G_full = nx.DiGraph()
        record_map: Dict[str, List[Dict[str, Any]]] = {}

        for row in reader:
            src = (row.get("input_address") or row.get("source_address") or "").strip()
            dst = (row.get("output_address") or row.get("destination_address") or "").strip()
            txid = (row.get("transaction_id") or row.get("tx_hash") or "tx_unk").strip()
            try:
                amt = float(row.get("amount_btc") or row.get("amount") or 1.0)
            except ValueError:
                amt = 1.0
            ts = (row.get("timestamp") or "2026-08-30T00:00:00Z").strip()
            scenario = (row.get("scenario") or row.get("label") or "normal").strip()

            if src and dst:
                G_full.add_edge(src, dst, txid=txid, amount=amt, timestamp=ts, scenario=scenario)

                rec = {"txid": txid, "amount": amt, "timestamp": ts, "scenario": scenario, "src": src, "dst": dst}
                record_map.setdefault(src, []).append(rec)
                record_map.setdefault(dst, []).append(rec)

        # Extract Neighborhood Sub-nodes around subject_id
        target_nodes: Set[str] = set()
        if subject_id in G_full:
            target_nodes.add(subject_id)
            # Add forward and backward neighbors up to 'hops'
            for h in range(1, hops + 1):
                new_nodes = set()
                for n in target_nodes:
                    if n in G_full:
                        new_nodes.update(G_full.successors(n))
                        new_nodes.update(G_full.predecessors(n))
                target_nodes.update(new_nodes)
        else:
            target_nodes = set(G_full.nodes)

        # Build Subgraph G
        G = G_full.subgraph(target_nodes).copy()

        # Compute Metrics on Subgraph
        pagerank_dict = {}
        try:
            if len(G.nodes) > 0:
                pagerank_dict = nx.pagerank(G, alpha=0.85)
        except Exception:
            pagerank_dict = {n: 1.0 / max(1, len(G.nodes)) for n in G.nodes}

        # Simple Cycle Detection
        cycles_found = []
        has_cycle = False
        nodes_in_cycles = set()
        try:
            for cycle in nx.simple_cycles(G):
                has_cycle = True
                cycles_found.append(cycle)
                for node in cycle:
                    nodes_in_cycles.add(node)
                if len(cycles_found) >= 5:
                    break
        except Exception:
            pass

        # Weakly connected components max size
        try:
            comps = list(nx.weakly_connected_components(G))
            max_comp_size = max(len(c) for c in comps) if comps else len(G.nodes)
        except Exception:
            max_comp_size = len(G.nodes)

        # Evaluate risk score for each node in G
        node_scores: Dict[str, int] = {}
        node_levels: Dict[str, str] = {}
        node_volumes: Dict[str, float] = {}
        node_signals: Dict[str, List[str]] = {}

        for n_id in list(G.nodes):
            records = record_map.get(n_id, [])
            total_vol = sum(r["amount"] for r in records)
            tx_cnt = len(records)
            node_volumes[n_id] = round(total_vol, 4)

            # Build context for risk evaluation
            context = {
                "amount_btc": records[0]["amount"] if records else 1.0,
                "inputs_count": G.in_degree(n_id),
                "outputs_count": G.out_degree(n_id),
                "tx_count_24h": tx_cnt,
                "volume_btc_24h": total_vol,
                "has_cycle": n_id in nodes_in_cycles,
                "pagerank": pagerank_dict.get(n_id, 0.0),
                "known_flagged_neighbor": n_id in FLAGGED_DEMO_ENTITIES
            }

            analysis = self.analysis_service.analyze_subject("address", n_id, context=context)
            node_scores[n_id] = analysis.risk_score
            node_levels[n_id] = analysis.risk_level
            node_signals[n_id] = [sig.title for sig in analysis.signals]

        # Apply Risk Filter if requested
        risk_filter_lower = risk_filter.lower()
        if risk_filter_lower in ["critical", "high", "medium", "low"]:
            filtered_nodes = {n for n, lvl in node_levels.items() if lvl == risk_filter_lower or n == subject_id}
            if filtered_nodes:
                G = G.subgraph(filtered_nodes).copy()

        # Truncation check
        is_truncated = False
        truncation_msg = None
        if len(G.nodes) > self.max_nodes:
            is_truncated = True
            truncation_msg = f"Graph display truncated at {self.max_nodes} nodes to ensure smooth browser rendering."
            kept_nodes = list(G.nodes)[:self.max_nodes]
            G = G.subgraph(kept_nodes).copy()

        # Format Cytoscape Nodes
        cytoscape_nodes: List[CytoscapeNodeWrapper] = []
        for n_id in G.nodes:
            in_deg = G.in_degree(n_id)
            out_deg = G.out_degree(n_id)
            pr = round(pagerank_dict.get(n_id, 0.0), 4)

            min_dist = None
            for flagged_id in FLAGGED_DEMO_ENTITIES.keys():
                if flagged_id in G:
                    try:
                        d = nx.shortest_path_length(G, source=n_id, target=flagged_id)
                        if min_dist is None or d < min_dist:
                            min_dist = d
                    except (nx.NetworkXNoPath, nx.NodeNotFound):
                        pass

            node_data = CytoscapeNodeData(
                id=n_id,
                label=n_id[:12] + "...",
                type="address",
                risk_level=node_levels.get(n_id, "low"),
                risk_score=node_scores.get(n_id, 10),
                amount_btc=node_volumes.get(n_id, 0.0),
                metadata=GraphNodeMetadata(
                    in_degree=in_deg,
                    out_degree=out_deg,
                    pagerank=pr,
                    shortest_distance_to_flagged=min_dist,
                    cluster_label=FLAGGED_DEMO_ENTITIES.get(n_id),
                    tx_count=G.in_degree(n_id) + G.out_degree(n_id),
                    volume_btc=node_volumes.get(n_id, 0.0),
                    signals=node_signals.get(n_id, [])
                )
            )
            cytoscape_nodes.append(CytoscapeNodeWrapper(data=node_data))

        # Format Cytoscape Edges
        cytoscape_edges: List[CytoscapeEdgeWrapper] = []
        for src, tgt, attr in G.edges(data=True):
            edge_data = CytoscapeEdgeData(
                id=f"{src}->{tgt}",
                source=src,
                target=tgt,
                txid=attr.get("txid", "tx_hash"),
                amount=attr.get("amount", 1.0),
                timestamp=attr.get("timestamp", "2026-08-30T00:00:00Z"),
                risk_level=node_levels.get(src, "low")
            )
            cytoscape_edges.append(CytoscapeEdgeWrapper(data=edge_data))

        flagged_count = sum(1 for n in G.nodes if n in FLAGGED_DEMO_ENTITIES)

        return GraphResponse(
            subject_type=subject_type,
            subject_id=subject_id,
            hops=hops,
            risk_filter=risk_filter,
            nodes=cytoscape_nodes,
            edges=cytoscape_edges,
            metrics=GraphMetricsSummary(
                total_nodes=len(cytoscape_nodes),
                total_edges=len(cytoscape_edges),
                has_cycle=has_cycle,
                cycles_found=cycles_found,
                max_component_size=max_comp_size,
                flagged_entities_count=flagged_count
            ),
            is_truncated=is_truncated,
            truncation_message=truncation_msg,
            disclaimer=RESPONSIBLE_AI_DISCLAIMER
        )

    def build_demo_graph(self, subject_type: str, subject_id: str, hops: int = 1, risk_filter: str = "all") -> GraphResponse:
        G = nx.DiGraph()
        nodes_data, edges_data = self._generate_topology(subject_id, hops)

        for n in nodes_data:
            G.add_node(n["id"], **n)
        for e in edges_data:
            G.add_edge(e["source"], e["target"], **e)

        pagerank_dict = {}
        try:
            if len(G.nodes) > 0:
                pagerank_dict = nx.pagerank(G, alpha=0.85)
        except Exception:
            pagerank_dict = {n: 1.0 / max(1, len(G.nodes)) for n in G.nodes}

        has_cycle = False
        cycles_found = []
        try:
            for c in nx.simple_cycles(G):
                has_cycle = True
                cycles_found.append(c)
                if len(cycles_found) >= 5:
                    break
        except Exception:
            has_cycle = False

        try:
            comps = list(nx.weakly_connected_components(G))
            max_comp_size = max(len(c) for c in comps) if comps else len(G.nodes)
        except Exception:
            max_comp_size = len(G.nodes)

        # Risk Filter
        risk_filter_lower = risk_filter.lower()
        if risk_filter_lower in ["critical", "high", "medium", "low"]:
            filtered_nodes = {n for n, data in G.nodes(data=True) if data.get("risk_level") == risk_filter_lower or n == subject_id}
            if filtered_nodes:
                G = G.subgraph(filtered_nodes).copy()

        # Truncation check
        is_truncated = False
        truncation_msg = None
        if len(G.nodes) > self.max_nodes:
            is_truncated = True
            truncation_msg = f"Graph display truncated at {self.max_nodes} nodes to ensure smooth browser rendering."
            kept_nodes = list(G.nodes)[:self.max_nodes]
            G = G.subgraph(kept_nodes).copy()

        cytoscape_nodes: List[CytoscapeNodeWrapper] = []
        for n_id in G.nodes:
            attr = G.nodes[n_id]
            in_deg = G.in_degree(n_id)
            out_deg = G.out_degree(n_id)
            pr = round(pagerank_dict.get(n_id, 0.0), 4)

            min_dist = None
            for flagged_id in FLAGGED_DEMO_ENTITIES.keys():
                if flagged_id in G:
                    try:
                        d = nx.shortest_path_length(G, source=n_id, target=flagged_id)
                        if min_dist is None or d < min_dist:
                            min_dist = d
                    except (nx.NetworkXNoPath, nx.NodeNotFound):
                        pass

            node_data = CytoscapeNodeData(
                id=n_id,
                label=attr.get("label", n_id[:10] + "..."),
                type=attr.get("type", "address"),
                risk_level=attr.get("risk_level", "low"),
                risk_score=attr.get("risk_score", 10),
                amount_btc=attr.get("amount_btc"),
                metadata=GraphNodeMetadata(
                    in_degree=in_deg,
                    out_degree=out_deg,
                    pagerank=pr,
                    shortest_distance_to_flagged=min_dist,
                    cluster_label=FLAGGED_DEMO_ENTITIES.get(n_id),
                    tx_count=in_deg + out_deg,
                    volume_btc=attr.get("amount_btc", 1.0) or 1.0,
                    signals=["High Fan-out Ratio", "Rapid Forwarding"] if attr.get("risk_score", 0) > 50 else []
                )
            )
            cytoscape_nodes.append(CytoscapeNodeWrapper(data=node_data))

        cytoscape_edges: List[CytoscapeEdgeWrapper] = []
        for src, tgt, attr in G.edges(data=True):
            edge_data = CytoscapeEdgeData(
                id=attr.get("id", f"{src}->{tgt}"),
                source=src,
                target=tgt,
                txid=attr.get("txid", "tx_hash_demo"),
                amount=attr.get("amount", 1.0),
                timestamp=attr.get("timestamp", "2026-08-27T00:00:00Z"),
                risk_level=attr.get("risk_level", "low")
            )
            cytoscape_edges.append(CytoscapeEdgeWrapper(data=edge_data))

        flagged_count = sum(1 for n in G.nodes if n in FLAGGED_DEMO_ENTITIES)

        return GraphResponse(
            subject_type=subject_type,
            subject_id=subject_id,
            hops=hops,
            risk_filter=risk_filter,
            nodes=cytoscape_nodes,
            edges=cytoscape_edges,
            metrics=GraphMetricsSummary(
                total_nodes=len(cytoscape_nodes),
                total_edges=len(cytoscape_edges),
                has_cycle=has_cycle,
                cycles_found=cycles_found,
                max_component_size=max_comp_size,
                flagged_entities_count=flagged_count
            ),
            is_truncated=is_truncated,
            truncation_message=truncation_msg,
            disclaimer=RESPONSIBLE_AI_DISCLAIMER
        )

    def _generate_topology(self, subject_id: str, hops: int) -> Tuple[List[Dict], List[Dict]]:
        nodes = []
        edges = []

        subject_risk = "high" if "9x08" in subject_id or "cycle" in subject_id else "medium"
        subject_score = 94 if "9x08" in subject_id else 68

        nodes.append({
            "id": subject_id,
            "label": subject_id[:12] + "...",
            "type": "address",
            "risk_level": subject_risk,
            "risk_score": subject_score,
            "amount_btc": 24.5
        })

        hop1_nodes = [
            {"id": f"bc1q_hop1_a_{subject_id[:6]}", "label": "Forwarding_Node_A", "type": "address", "risk_level": "medium", "risk_score": 45, "amount_btc": 12.0},
            {"id": f"bc1q_hop1_b_{subject_id[:6]}", "label": "Destination_Node_B", "type": "address", "risk_level": "low", "risk_score": 15, "amount_btc": 8.5},
            {"id": "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0", "label": "Ransomware_Payout_01", "type": "address", "risk_level": "critical", "risk_score": 94, "amount_btc": 4.85},
        ]

        for h1 in hop1_nodes:
            if h1["id"] != subject_id:
                nodes.append(h1)
                edges.append({
                    "id": f"edge_{subject_id[:6]}_{h1['id'][:6]}",
                    "source": subject_id,
                    "target": h1["id"],
                    "txid": f"tx_h1_{h1['id'][:6]}",
                    "amount": h1["amount_btc"],
                    "timestamp": "2026-08-27T08:00:00Z",
                    "risk_level": h1["risk_level"]
                })

        if "cycle" in subject_id or "loop" in subject_id:
            h1_a_id = f"bc1q_hop1_a_{subject_id[:6]}"
            h1_b_id = f"bc1q_hop1_b_{subject_id[:6]}"
            edges.append({
                "id": f"cycle_back_{h1_b_id[:6]}_{subject_id[:6]}",
                "source": h1_b_id,
                "target": subject_id,
                "txid": "tx_cycle_return",
                "amount": 10.0,
                "timestamp": "2026-08-27T09:00:00Z",
                "risk_level": "high"
            })

        if hops >= 2:
            for i, h1 in enumerate(hop1_nodes):
                h2_id = f"bc1q_hop2_{i}_{subject_id[:4]}"
                nodes.append({
                    "id": h2_id,
                    "label": f"Deep_Entity_{i+1}",
                    "type": "address",
                    "risk_level": "low",
                    "risk_score": 12,
                    "amount_btc": 3.2
                })
                edges.append({
                    "id": f"edge_h2_{h1['id'][:6]}_{h2_id[:6]}",
                    "source": h1["id"],
                    "target": h2_id,
                    "txid": f"tx_h2_{i}",
                    "amount": 3.2,
                    "timestamp": "2026-08-27T10:00:00Z",
                    "risk_level": "low"
                })

        unique_nodes = {n["id"]: n for n in nodes}.values()
        return list(unique_nodes), edges
