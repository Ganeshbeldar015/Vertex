---
status: complete
owner: tech-lead
task: T-0001
acceptance_refs:
  - AC-001-a
  - AC-002-a
  - AC-003-a
  - AC-004-a
  - AC-005-a
---

# 03-Plan: Walking Skeleton Technical Plan

## 1. Technical Approach
Implement the walking skeleton in modular Python components using an in-memory graph engine with Cypher-style query matching, pure JSON-RPC tool dispatch, and an async agent loop. This guarantees self-contained execution and instant test feedback (< 1s) while adhering to future FalkorDB and MCP integration points.

## 2. File-Level Decomposition
1. `src/graph/engine.py`:
   - PropertyGraph class storing nodes, relationships, and property indexes.
   - Parameterized query method `execute_cypher(query, params)`.
   - Multi-hop traversal helper for neighborhood expansion.
2. `src/data/generator.py`:
   - `generate_synthetic_network(seed=42)`: Populates nodes and relationships.
   - Seeds hero case: `A-1042` and `A-1050` sharing device `D-77`, with outgoing transfer from `A-1050` to `A-1061`.
3. `src/mcp/server.py`:
   - Tool handlers: `get_entity` and `expand_neighborhood`.
   - JSON-RPC compatible schema definitions.
4. `src/agent/loop.py`:
   - `InvestigationAgent`: Receives alert, calls MCP tools via dispatch interface, builds working memory, evaluates ring hypotheses, returns structured verdict.
5. `src/agent/verifier.py`:
   - `verify_citations(rationale, tool_outputs)`: Validates that all evidence IDs and entity references exist in observed tool results.

## 3. Lane Allocation & Locks
- **Lane `main`:**
  - Owner: `builder`
  - Owned paths: `src/graph/**`, `src/data/**`, `src/mcp/**`, `src/agent/**`
  - Lock recorded in: `harness/state/locks/main.json`

## 4. Test Strategy per AC
- **AC-001-a:** `test_synthetic_generator_creates_hero_ring` asserts counts and hero nodes exist.
- **AC-002-a:** `test_graph_engine_parameterized_query` asserts parameterized queries return correct data and rejects string injection.
- **AC-003-a:** `test_mcp_tool_dispatch` asserts tool schemas and successful responses for `get_entity` and `expand_neighborhood`.
- **AC-004-a:** `test_agent_investigation_finds_ring` asserts multi-hop discovery of `D-77` and `A-1050`.
- **AC-005-a:** `test_citation_verifier_validates_evidence` asserts verifier passes on true evidence and fails on hallucinated IDs.
