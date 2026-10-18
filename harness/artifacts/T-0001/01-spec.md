---
status: complete
owner: po-spec
task: T-0001
acceptance_refs:
  - AC-001-a
  - AC-002-a
  - AC-003-a
  - AC-004-a
  - AC-005-a
---

# 01-Spec: Walking Skeleton (End-to-End Slice)

## 1. Intent & Problem Summary
Deliver a functional, tested walking skeleton of the GraphSleuth fraud investigation agent. When an alert triggers on an account, the system traverses the connected graph across multi-hop relationships via an MCP tool server, extracts an evidence subgraph, formulates hypotheses, and delivers an explainable verdict with cited evidence IDs.

## 2. Scope Boundaries
- **In Scope:**
  - Synthetic data generator producing accounts, devices, and transactions with 1 seeded multi-hop fraud chain.
  - In-memory property graph engine supporting node/relationship storage and parameterized Cypher queries.
  - SENGRA MCP tool server providing `get_entity` and `expand_neighborhood` tools.
  - Agent loop executing plan -> tool selection -> multi-hop observation -> structured verdict.
  - Citation verification asserting that 100% of cited evidence IDs map to tool outputs.
- **Out of Scope:**
  - Community detection algorithms (Louvain) and cycle detection (deferred to Sprint 2).
  - External core banking API mutations (deferred to Sprint 3).
  - Full React UI (deferred to Sprint 4).

## 3. User Stories
- **US-1.1 (Alert Investigation):** As an analyst, I provide an alert ID (`ALT-101` on Account `A-1042`), and the agent executes multi-hop graph expansion to find connected accounts and devices.
- **US-1.2 (MCP Tool Dispatch):** As an agent, I discover and call `get_entity` and `expand_neighborhood` via standard MCP schemas to query the graph.
- **US-1.3 (Verifiable Findings):** As an auditor, I inspect the agent's verdict and confirm that every cited claim references verified evidence IDs (`E1`, `E2`).

## 4. Requirement to Acceptance Mapping

| Requirement | Acceptance ID | Given / When / Then Specification |
|---|---|---|
| **REQ-001** (Data Generation) | **AC-001-a** | **Given** data generation parameters, **When** synthetic generator runs, **Then** it produces account nodes (`A-1042`, `A-1050`, `A-1061`), device node (`D-77`), and transaction edges creating a 3-hop link. |
| **REQ-002** (Graph Store) | **AC-002-a** | **Given** the generated nodes and edges, **When** loaded into graph store, **Then** parameterized queries return exact node properties and edge relationships. |
| **REQ-004** (MCP Tools) | **AC-003-a** | **Given** the SENGRA MCP server running, **When** client invokes `get_entity` or `expand_neighborhood`, **Then** server returns structured graph records conforming to JSON schemas. |
| **REQ-008** (Agent Loop) | **AC-004-a** | **Given** an initial alert on `A-1042`, **When** agent loop executes, **Then** it performs <= 15 tool calls, discovers `D-77` and `A-1050`, and outputs a verdict with risk confidence. |
| **REQ-013** (Explanation & Citation) | **AC-005-a** | **Given** the agent's explanation text citing evidence IDs, **When** citation verifier runs, **Then** 100% of cited IDs match actual tool outputs. |

## 5. Edge Cases & Constraints
- Empty neighborhood: Agent must handle isolated accounts gracefully without crashing.
- Budget overrun: Agent must terminate gracefully if step limit is reached.
- Query injection: Cypher queries must reject unparameterized string injections.

## 6. Open Questions
*(None — specifications fully aligned with PRD and MCP guide.)*
