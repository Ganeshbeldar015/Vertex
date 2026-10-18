"""Unit tests for T-0001 Walking Skeleton (End-to-End Slice)."""
import pytest
from src.data.generator import generate_synthetic_network
from src.graph.engine import PropertyGraph
from src.mcp.server import SengraMCPServer
from src.agent.loop import InvestigationAgent
from src.agent.verifier import verify_citations


def test_synthetic_generator_creates_hero_ring():
    """AC-001-a: Data generator creates accounts, devices, and hero fraud ring."""
    data = generate_synthetic_network(seed=42)
    assert "nodes" in data and "edges" in data

    # Verify hero nodes exist
    node_ids = {n["id"] for n in data["nodes"]}
    assert "A-1042" in node_ids
    assert "A-1050" in node_ids
    assert "A-1061" in node_ids
    assert "D-77" in node_ids

    # Verify hero edges: A-1042 -> D-77 and A-1050 -> D-77
    device_edges = [
        e for e in data["edges"]
        if e["type"] == "USED_DEVICE" and e["target"] == "D-77"
    ]
    sources = {e["source"] for e in device_edges}
    assert "A-1042" in sources
    assert "A-1050" in sources

    # Verify transfer from A-1050 to A-1061
    transfer_edges = [
        e for e in data["edges"]
        if e["type"] == "TRANSFERRED_TO" and e["source"] == "A-1050" and e["target"] == "A-1061"
    ]
    assert len(transfer_edges) == 1


def test_graph_engine_parameterized_query():
    """AC-002-a: Graph engine executes parameterized Cypher queries."""
    graph = PropertyGraph()
    graph.add_node("A-1042", ["Account"], {"balance": 1500.0, "risk_score": 0.3})
    graph.add_node("D-77", ["Device"], {"fingerprint": "fp_xyz"})
    graph.add_edge("A-1042", "D-77", "USED_DEVICE", {})

    # Parameterized node fetch
    res = graph.query("MATCH (a:Account {id: $id}) RETURN a", {"id": "A-1042"})
    assert len(res) == 1
    assert res[0]["id"] == "A-1042"
    assert res[0]["properties"]["balance"] == 1500.0

    # Reject unparameterized query attempting write
    with pytest.raises(ValueError, match="Write keywords forbidden in read-only query"):
        graph.query("CREATE (n:BadNode)")


def test_mcp_tool_dispatch():
    """AC-003-a: MCP server handles get_entity and expand_neighborhood."""
    data = generate_synthetic_network(seed=42)
    graph = PropertyGraph()
    graph.load_dataset(data)
    server = SengraMCPServer(graph)

    # get_entity
    entity_res = server.handle_call("graph.get_entity", {"entity_id": "A-1042"})
    assert entity_res["status"] == "ok"
    assert entity_res["result"]["id"] == "A-1042"

    # expand_neighborhood
    expand_res = server.handle_call("graph.expand_neighborhood", {"entity_id": "A-1042", "hops": 2})
    assert expand_res["status"] == "ok"
    subgraph = expand_res["result"]
    sub_node_ids = {n["id"] for n in subgraph["nodes"]}
    assert "D-77" in sub_node_ids
    assert "A-1050" in sub_node_ids


def test_agent_investigation_finds_ring():
    """AC-004-a: Agent conducts multi-hop investigation on alert A-1042 and detects ring."""
    data = generate_synthetic_network(seed=42)
    graph = PropertyGraph()
    graph.load_dataset(data)
    server = SengraMCPServer(graph)
    agent = InvestigationAgent(tool_client=server)

    investigation = agent.investigate_alert(alert_id="ALT-101", target_account_id="A-1042")
    assert investigation["status"] == "completed"
    assert investigation["verdict"] == "fraud_ring_detected"
    assert investigation["confidence"] >= 0.75
    assert "A-1050" in investigation["discovered_entities"]
    assert "D-77" in investigation["discovered_entities"]
    assert len(investigation["tool_calls"]) <= 15
    assert len(investigation["evidence_subgraph"]["nodes"]) >= 3


def test_citation_verifier_validates_evidence():
    """AC-005-a: Citation verifier validates all referenced entities exist in tool outputs."""
    tool_outputs = {
        "nodes": [{"id": "A-1042"}, {"id": "A-1050"}, {"id": "D-77"}],
        "edges": [{"source": "A-1042", "target": "D-77"}]
    }

    # True citation rationale
    valid_rationale = "Account A-1042 shares device D-77 with Account A-1050."
    res = verify_citations(valid_rationale, tool_outputs)
    assert res["valid"] is True
    assert len(res["unsupported_ids"]) == 0

    # Hallucinated citation
    invalid_rationale = "Account A-1042 transferred funds to phantom account A-9999."
    res_invalid = verify_citations(invalid_rationale, tool_outputs)
    assert res_invalid["valid"] is False
    assert "A-9999" in res_invalid["unsupported_ids"]
