---
status: complete
owner: tech-lead
task: T-0002
acceptance_refs:
  - AC-002-b
  - AC-002-c
  - AC-002-d
  - AC-002-e
  - AC-002-f
---

# 03-Plan: Core Graph Algorithms & MCP Implementation Plan

## 1. Technical Strategy
Implement high-performance, deterministic graph algorithms in pure Python within `src/graph/algorithms.py`. This avoids heavy C++ runtime dependencies while guaranteeing exact reproducible outputs for testing and CI. Integrate these algorithms directly into `PropertyGraph` and expose them via `SengraMCPServer` under standard namespaced tool handlers (`algo.*` and `graph.*`).

## 2. File-Level Decomposition
1. `src/graph/algorithms.py`:
   - `detect_communities(graph, subgraph_nodes=None)`: Label propagation algorithm iteratively updating node labels to majority neighbor labels.
   - `rank_centrality(graph, subgraph_nodes=None, damping_factor=0.85, max_iter=20)`: Power iteration PageRank computing transition probability over directed edges.
   - `detect_cycles(graph, start_node=None, min_len=3, max_len=6)`: Recursive DFS cycle finding on `TRANSFERRED_TO` relationships.
   - `find_paths(graph, source_id, target_id, max_hops=4)`: BFS shortest path finding returning node sequence and connecting edges.
   - `find_shared_attributes(graph, entity_id, attribute_type="Device")`: Inverted lookup finding peer accounts that connect to the same attribute nodes.
2. `src/graph/engine.py`:
   - Add helper methods to delegate to `algorithms.py`.
   - Enhance `query()` method to support general read-only queries with parameters while enforcing mutation keyword rejection.
3. `src/mcp/server.py`:
   - Register 6 new tools in `list_tools()` with complete JSON schemas.
   - Add dispatch branches in `handle_call()` for:
     - `algo.detect_communities`
     - `algo.rank_centrality`
     - `algo.detect_cycles`
     - `graph.find_paths`
     - `graph.shared_attributes`
     - `graph.run_readonly_cypher`

## 3. Lane Allocation & Ownership
- **Lane `main`:**
  - Owner: `builder`
  - Owned paths: `src/graph/**`, `src/mcp/**`
  - Lock recorded in: `harness/state/locks/main.json`

## 4. Test Strategy per AC
- **AC-002-b:** `test_detect_communities_clusters_ring` tests community detection clusters hero ring nodes.
- **AC-002-c:** `test_rank_centrality_identifies_hub` tests PageRank ranks transit nodes higher than peripheral nodes.
- **AC-002-d:** `test_detect_cycles_finds_circular_transfers` tests finding the 3-node cycle `A-1042 -> A-1050 -> A-1061 -> A-1042`.
- **AC-002-e:** `test_find_paths_returns_shortest_connection` tests shortest path traversal between `A-1042` and `A-1061`.
- **AC-002-f:** `test_shared_attributes_finds_colocated_accounts` & `test_run_readonly_cypher_guards` tests attribute lookup and keyword security guards.
