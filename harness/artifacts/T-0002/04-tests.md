---
status: complete
owner: test-author
task: T-0002
acceptance_refs:
  - AC-002-b
  - AC-002-c
  - AC-002-d
  - AC-002-e
  - AC-002-f
---

# 04-Tests: Core Graph Algorithms Red Test Suite

## 1. Acceptance Criteria to Test Matrix

| AC ID | Test Function | Test File | Target Module |
|---|---|---|---|
| **AC-002-b** | `test_detect_communities_clusters_ring` | `tests/unit/test_graph_algorithms.py` | `src.graph.algorithms.detect_communities` |
| **AC-002-c** | `test_rank_centrality_identifies_hub` | `tests/unit/test_graph_algorithms.py` | `src.graph.algorithms.rank_centrality` |
| **AC-002-d** | `test_detect_cycles_finds_circular_transfers` | `tests/unit/test_graph_algorithms.py` | `src.graph.algorithms.detect_cycles` |
| **AC-002-e** | `test_find_paths_returns_shortest_connection` | `tests/unit/test_graph_algorithms.py` | `src.graph.algorithms.find_paths` |
| **AC-002-f** | `test_shared_attributes_finds_colocated_accounts` | `tests/unit/test_graph_algorithms.py` | `src.graph.algorithms.find_shared_attributes` |
| **AC-002-f** | `test_run_readonly_cypher_guards_and_executes` | `tests/unit/test_graph_algorithms.py` | `src.mcp.server` |
| **Contract** | `test_mcp_server_dispatches_all_new_tools` | `tests/unit/test_graph_algorithms.py` | `src.mcp.server.SengraMCPServer` |

## 2. Red Test Run Evidence

```
$ python -m pytest tests/unit/test_graph_algorithms.py
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1
collected 0 items / 1 error

=================================== ERRORS ====================================
ERROR collecting tests/unit/test_graph_algorithms.py
E   ModuleNotFoundError: No module named 'src.graph.algorithms'
============================== 1 error in 0.25s ===============================
Exit Code: 1 (Failing - Red)
```

## 3. Test Determinism & Constraints
- Hermetic in-memory graph fixture (`fraud_graph`).
- Seed fixed at 42.
- Zero network or disk I/O; sub-second execution.
