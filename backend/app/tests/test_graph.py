from fastapi.testclient import TestClient
from app.main import app
from app.services.graph.graph_service import GraphService

client = TestClient(app)

def test_graph_endpoint_1_hop():
    response = client.get("/api/v1/graph/address/bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0?hops=1")
    assert response.status_code == 200
    data = response.json()
    assert data["subject_id"] == "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0"
    assert data["hops"] == 1
    assert len(data["nodes"]) > 0
    assert len(data["edges"]) > 0
    assert "metrics" in data
    assert data["metrics"]["total_nodes"] == len(data["nodes"])

def test_graph_endpoint_2_hop():
    response = client.get("/api/v1/graph/address/bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0?hops=2")
    assert response.status_code == 200
    data = response.json()
    assert data["hops"] == 2
    assert len(data["nodes"]) > 3 # 2-hop should have more nodes than 1-hop

def test_directed_graph_direction_and_cycles():
    graph_service = GraphService()
    res = graph_service.build_demo_graph("address", "bc1qcycle000111222333444555666777888999", hops=1)
    assert res.metrics.has_cycle is True
    assert len(res.metrics.cycles_found) > 0

def test_node_capping_and_truncation():
    # Set artificial small node cap of 2 nodes
    graph_service = GraphService(max_nodes=2)
    res = graph_service.build_demo_graph("address", "bc1q9x087v2n5k4h3j2m1p9l8k7j6h5g4f3d2s1a0", hops=2)
    assert res.is_truncated is True
    assert res.truncation_message is not None
    assert len(res.nodes) <= 2

def test_cytoscape_wrapper_schema():
    response = client.get("/api/v1/graph/address/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa?hops=1")
    assert response.status_code == 200
    data = response.json()
    first_node = data["nodes"][0]["data"]
    assert "id" in first_node
    assert "type" in first_node
    assert "risk_level" in first_node
    assert "metadata" in first_node
    assert "pagerank" in first_node["metadata"]
