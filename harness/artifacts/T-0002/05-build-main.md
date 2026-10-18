---
status: complete
owner: builder
task: T-0002
lane: main
acceptance_refs:
  - AC-002-b
  - AC-002-c
  - AC-002-d
  - AC-002-e
  - AC-002-f
---

# 05-Build-Main: Core Graph Algorithms & MCP Tools Implementation

## 1. Summary of Changes
Implemented the core graph analysis algorithms and MCP tools in `src/graph/algorithms.py` and `src/mcp/server.py`:
- `detect_communities`: Pure Python label propagation clustering accounts sharing devices and circular transfers.
- `rank_centrality`: PageRank power iteration identifying transaction hubs and money routing nodes.
- `detect_cycles`: DFS cycle finder isolating circular transfer paths (`A-1042 -> A-1050 -> A-1061 -> A-1042`).
- `find_paths`: BFS shortest pathfinder across multi-hop edges.
- `find_shared_attributes`: Inverted index query linking accounts co-located on devices, IPs, addresses.
- `SengraMCPServer`: Exposed all tools under `algo.*` and `graph.*` namespaces with complete JSON schema validation and read-only error handling.

## 2. Test Execution & Verification (Green Run)
```
$ python -m pytest tests/unit/test_graph_algorithms.py
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1
collected 7 items

tests/unit/test_graph_algorithms.py .......                              [100%]

============================== 7 passed in 0.05s ==============================
```

## 3. Parameter Safety & Injection Defense
- Query parameters strictly bound via `$param` mapping in `PropertyGraph.query()`.
- Mutation keywords (`CREATE`, `MERGE`, `DELETE`, etc.) actively blocked and tested.

## 4. Commands Run
- `pytest tests/unit/test_graph_algorithms.py` -> 7 passed (exit 0)
- `pytest tests/` -> 32 passed (exit 0)
- `python scripts/check_harness.py` -> 0 problems (exit 0)
