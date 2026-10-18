# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [0.3.0] - 2026-10-18
### Added
- Composite risk scoring tool (`src/graph/risk.py`, `algo.score_risk`) evaluating shared devices, circular flows, community density, and transaction velocity.
- Core banking action service (`src/actions/service.py`) with approval state machine, idempotency, reversibility (`unfreeze`, `unblock`), and immutable `ActionLog`.
- MCP tools for remediation actions (`action.create_case`, `action.flag_entity`, `action.freeze_account`, `action.block_device`, `action.approve_action`, `action.reverse_action`, `action.get_audit_log`).
- Multi-hop hypothesis testing loop in `src/agent/loop.py` systematically validating fraud ring hypotheses and recommending actions.
- Unit test suite `tests/unit/test_reasoning_and_actions.py` covering risk scoring, hypothesis loops, action gating, and audit logging.

## [0.2.0] - 2026-10-18
### Added
- Core graph algorithms module (`src/graph/algorithms.py`):
  - `algo.detect_communities`: Label propagation community detection clustering fraud rings.
  - `algo.rank_centrality`: PageRank centrality scoring money hubs and transaction routers.
  - `algo.detect_cycles`: DFS cycle detector isolating circular money laundering loops.
  - `graph.find_paths`: BFS shortest pathfinder across multi-hop relationships.
  - `graph.shared_attributes`: Inverted attribute index linking accounts sharing devices/IPs.
  - `graph.run_readonly_cypher`: Guarded Cypher query tool with active mutation blocking.
- Unit tests in `tests/unit/test_graph_algorithms.py` covering all algorithmic acceptance criteria.

## [0.1.0] - 2026-10-18
### Added
- Harness infrastructure (G0–G5 gates, path guard, circuit breaker, `.mcp.json`).
- Synthetic fraud data generator with seeded hero fraud ring (`A-1042`, `A-1050`, `D-77`, `A-1061`).
- Property graph engine with OpenCypher queries, parameter binding, and neighborhood expansion.
- SENGRA MCP tool server implementing `graph.get_entity` and `graph.expand_neighborhood`.
- Autonomous multi-hop investigation agent loop.
- Citation verifier guaranteeing 100% verified evidence claims.
