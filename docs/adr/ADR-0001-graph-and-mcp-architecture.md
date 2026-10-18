# ADR-0001: Graph Engine and MCP Architecture

## Status
Accepted

## Context
Financial fraud ring detection requires discovering multi-hop topologies (shared devices, circular transfers) that cannot be retrieved effectively via relational SQL joins or vector embeddings alone. Furthermore, tools must be discoverable and invocable via standard protocols.

## Decision
1. Use FalkorDB / OpenCypher property graph model with derived `TRANSFERRED_TO` edges for 1-hop path traversal.
2. Expose all 15 investigation capabilities (`graph.*`, `algo.*`, `action.*`) through the Model Context Protocol (MCP) using `@falkordb/mcpserver` and custom Python MCP server endpoints.
3. Enforce read-only database connections by default for agents, requiring explicit confirmation for write operations.

## Consequences
- High performance on multi-hop pathfinding.
- Standardized tool integration across LLM clients.
- Prevents accidental data alteration through strict read-only default permissions.
