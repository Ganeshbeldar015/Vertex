---
status: complete
owner: scribe
task: T-0002
acceptance_refs:
  - AC-002-b
  - AC-002-c
  - AC-002-d
  - AC-002-e
  - AC-002-f
---

# 08-Docs: Core Graph Algorithms Documentation

## 1. Documentation Updates
- Updated `README.md` detailing the 6 new graph analysis tools and algorithms.
- Added entry to `CHANGELOG.md` under `[0.2.0] - 2026-10-18`.

## 2. API & Tool Catalog Documentation
- **`algo.detect_communities`**: Detects colluding account communities via label propagation.
- **`algo.rank_centrality`**: PageRank algorithm ranking transaction hubs.
- **`algo.detect_cycles`**: DFS cycle detector finding circular money flows.
- **`graph.find_paths`**: BFS pathfinder for shortest relationship paths.
- **`graph.shared_attributes`**: Inverted index query identifying accounts sharing devices or IPs.
- **`graph.run_readonly_cypher`**: Guarded parameterized Cypher evaluator.
