from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class GraphNodeMetadata(BaseModel):
    in_degree: int = 0
    out_degree: int = 0
    pagerank: float = 0.0
    shortest_distance_to_flagged: Optional[int] = None
    cluster_label: Optional[str] = None
    tx_count: int = 0
    volume_btc: float = 0.0
    signals: List[str] = []

class CytoscapeNodeData(BaseModel):
    id: str
    label: str
    type: str # 'address' or 'transaction'
    risk_level: str # low, medium, high, critical, unknown
    risk_score: int
    amount_btc: Optional[float] = None
    metadata: GraphNodeMetadata

class CytoscapeNodeWrapper(BaseModel):
    data: CytoscapeNodeData

class CytoscapeEdgeData(BaseModel):
    id: str
    source: str
    target: str
    txid: str
    amount: float
    timestamp: str
    risk_level: str

class CytoscapeEdgeWrapper(BaseModel):
    data: CytoscapeEdgeData

class GraphMetricsSummary(BaseModel):
    total_nodes: int
    total_edges: int
    has_cycle: bool
    cycles_found: List[List[str]] = []
    max_component_size: int
    flagged_entities_count: int

class GraphResponse(BaseModel):
    subject_type: str
    subject_id: str
    hops: int
    risk_filter: str = "all"
    nodes: List[CytoscapeNodeWrapper]
    edges: List[CytoscapeEdgeWrapper]
    metrics: GraphMetricsSummary
    is_truncated: bool = False
    truncation_message: Optional[str] = None
    disclaimer: str
