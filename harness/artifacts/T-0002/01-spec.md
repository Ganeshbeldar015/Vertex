---
status: complete
owner: po-spec
task: T-0002
acceptance_refs:
  - AC-002-b
  - AC-002-c
  - AC-002-d
  - AC-002-e
  - AC-002-f
---

# 01-Spec: Core Graph Algorithms & MCP Tools

## 1. Intent & Problem Summary
Enable advanced graph analysis capabilities for fraud investigation by exposing graph algorithms (community detection, centrality, cycle detection, pathfinding) and specialized queries as standard MCP tools. These tools allow the agent to detect hidden multi-hop fraud communities, isolate ring members, measure transaction concentration, and trace circular money laundering loops.

## 2. Scope Boundaries
- **In Scope:**
  - `algo.detect_communities`: Identifies dense clusters of connected entities using modularity/label propagation.
  - `algo.rank_centrality`: Computes PageRank centrality to identify money hubs and transaction distributors.
  - `algo.detect_cycles`: Detects closed loops of money transfers (cycles of length 3 to 6).
  - `graph.find_paths`: Finds shortest path and all paths between two entities across relationships.
  - `graph.shared_attributes`: Finds entities sharing devices, IPs, addresses, or phone numbers.
  - `graph.run_readonly_cypher`: Guarded execution of arbitrary read Cypher with keyword validation and LIMIT.
  - Full schema registration in `SengraMCPServer`.
- **Out of Scope:**
  - Automated action execution and approval workflows (Sprint 3).
  - Full frontend visual canvas (Sprint 4).

## 3. User Stories
- **US-2.1 (Community Discovery):** As an analyst, I want to detect if an alerted account belongs to a dense cluster of colluding accounts sharing devices and funds.
- **US-2.2 (Hub & Mule Identification):** As an analyst, I want to rank accounts in a cluster by centrality to identify the central organizer or cash-out mule.
- **US-2.3 (Circular Money Tracing):** As an analyst, I want to find circular money flows where stolen funds loop back to their source or intermediate layers.
- **US-2.4 (Path Inspection):** As an analyst, I want to trace the shortest path connecting two suspect accounts across devices and transfers.

## 4. Requirement to Acceptance Mapping

| Requirement | Acceptance ID | Given / When / Then Specification |
|---|---|---|
| **REQ-005** (Community Detection) | **AC-002-b** | **Given** a graph containing hero fraud accounts and legitimate nodes, **When** `algo.detect_communities` is called, **Then** `A-1042`, `A-1050`, and `A-1061` are assigned to the same community with high internal edge density. |
| **REQ-005** (Centrality Ranking) | **AC-002-c** | **Given** a graph with transfer flows, **When** `algo.rank_centrality` is called, **Then** accounts acting as transit hubs receive higher PageRank scores than leaf nodes. |
| **REQ-005** (Cycle Detection) | **AC-002-d** | **Given** circular transfers `A-1042 -> A-1050 -> A-1061 -> A-1042`, **When** `algo.detect_cycles` is executed, **Then** the cycle is returned with node sequence and transfer amounts. |
| **REQ-005** (Pathfinding) | **AC-002-e** | **Given** accounts `A-1042` and `A-1061`, **When** `graph.find_paths` is called, **Then** shortest connecting paths across `TRANSFERRED_TO` and `USED_DEVICE` are returned. |
| **REQ-004 & REQ-006** (Shared Attributes & Cypher) | **AC-002-f** | **Given** account `A-1042`, **When** `graph.shared_attributes` runs, **Then** co-located account `A-1050` is returned via device `D-77`; `graph.run_readonly_cypher` executes read queries and throws errors on write queries. |

## 5. Edge Cases & Constraints
- Disconnected components: Algorithms must handle disconnected subgraphs without errors.
- Self-loops: Must be excluded from cycle detection.
- Max execution time: Graph algorithms must complete within <= 2s per tool call.
