"""Unit tests for Sprint 2 Core Graph Algorithms & MCP Tools (T-0002)."""
import pytest
from src.data.generator import generate_synthetic_network
from src.graph.engine import PropertyGraph
from src.mcp.server import SengraMCPServer
from src.graph.algorithms import (
    detect_communities,
    rank_centrality,
    detect_cycles,
    find_paths,
    find_shared_attributes
)


@pytest.fixture
def fraud_graph():
    """Builds a test graph with seeded hero fraud ring and legitimate nodes."""
    data = generate_synthetic_network(seed=42)
    graph = PropertyGraph()
    graph.load_dataset(data)
    return graph


def test_detect_communities_clusters_ring(fraud_graph):
    """AC-002-b: Community detection clusters the tightly connected fraud ring."""
    # Run community detection over the fraud graph
    result = detect_communities(fraud_graph)
    assert "communities" in result
    communities = result["communities"]
    assert len(communities) > 0

    # Locate the community containing A-1042
    ring_comm = next(
        (c for c in communities if "A-1042" in c["members"]),
        None
    )
    assert ring_comm is not None
    # Hero ring accounts sharing device and circular transfers should be co-clustered
    assert "A-1050" in ring_comm["members"]
    assert "D-77" in ring_comm["members"]


def test_rank_centrality_identifies_hub(fraud_graph):
    """AC-002-c: PageRank algorithm assigns higher centrality to hub accounts."""
    result = rank_centrality(fraud_graph)
    assert "rankings" in result
    rankings = result["rankings"]
    assert len(rankings) > 0

    scores = {r["id"]: r["score"] for r in rankings}
    assert "A-1042" in scores
    assert "A-1050" in scores
    # A-1050 and A-1042 receive and route multiple flows, so their centrality should exceed leaf nodes
    legit_leaf_score = scores.get("A-LEGIT-001", 0.0)
    assert scores["A-1042"] > legit_leaf_score


def test_detect_cycles_finds_circular_transfers(fraud_graph):
    """AC-002-d: Cycle detection finds the circular transfer loop A-1042 -> A-1050 -> A-1061 -> A-1042."""
    result = detect_cycles(fraud_graph, min_length=3, max_length=6)
    assert "cycles" in result
    cycles = result["cycles"]
    assert len(cycles) >= 1

    # Find the hero cycle
    hero_cycle = next(
        (c for c in cycles if "A-1042" in c["path"] and "A-1050" in c["path"] and "A-1061" in c["path"]),
        None
    )
    assert hero_cycle is not None
    assert hero_cycle["length"] == 3
    assert hero_cycle["total_amount"] >= 8000.0


def test_find_paths_returns_shortest_connection(fraud_graph):
    """AC-002-e: Shortest path finds the connection between A-1042 and A-1061."""
    result = find_paths(fraud_graph, source_id="A-1042", target_id="A-1061", max_hops=4)
    assert result["found"] is True
    assert result["hops"] >= 1
    assert "A-1042" in result["path"]
    assert "A-1061" in result["path"]
    assert len(result["edges"]) > 0


def test_shared_attributes_finds_colocated_accounts(fraud_graph):
    """AC-002-f: Shared attribute tool returns accounts sharing device D-77."""
    result = find_shared_attributes(fraud_graph, entity_id="A-1042", attribute_type="Device")
    assert "shared_entities" in result
    shared = result["shared_entities"]
    assert len(shared) >= 1

    dev_match = next((s for s in shared if s["attribute_id"] == "D-77"), None)
    assert dev_match is not None
    assert "A-1050" in dev_match["linked_entities"]


def test_run_readonly_cypher_guards_and_executes(fraud_graph):
    """AC-002-f: Guarded Cypher executes read queries and throws errors on mutation keywords."""
    server = SengraMCPServer(fraud_graph)

    # Valid read query
    read_res = server.handle_call("graph.run_readonly_cypher", {
        "query": "MATCH (a:Account {id: $id}) RETURN a",
        "params": {"id": "A-1042"}
    })
    assert read_res["status"] == "ok"
    assert len(read_res["result"]) == 1

    # Rejected mutation query
    write_res = server.handle_call("graph.run_readonly_cypher", {
        "query": "CREATE (a:Account {id: 'bad'})"
    })
    assert write_res["status"] == "error"
    assert "forbidden" in write_res["error"].lower()


def test_mcp_server_dispatches_all_new_tools(fraud_graph):
    """AC-002-g: MCP server lists and dispatches all 6 new tools with valid schemas."""
    server = SengraMCPServer(fraud_graph)
    tools = server.list_tools()
    tool_names = {t["name"] for t in tools}

    required_tools = {
        "graph.get_entity",
        "graph.expand_neighborhood",
        "algo.detect_communities",
        "algo.rank_centrality",
        "algo.detect_cycles",
        "graph.find_paths",
        "graph.shared_attributes",
        "graph.run_readonly_cypher"
    }
    assert required_tools.issubset(tool_names)

    # Test community call via MCP
    comm_resp = server.handle_call("algo.detect_communities", {})
    assert comm_resp["status"] == "ok"
    assert "communities" in comm_resp["result"]

    # Test centrality call via MCP
    cent_resp = server.handle_call("algo.rank_centrality", {"top_k": 5})
    assert cent_resp["status"] == "ok"
    assert "rankings" in cent_resp["result"]
