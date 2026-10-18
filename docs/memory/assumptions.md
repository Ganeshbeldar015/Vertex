# Assumptions Log

> Record of operational and technical assumptions.

- **[ASM-001]** FalkorDB and Redis OpenCypher interface are the primary graph query engine; local test runs may use in-memory/fallback graph structures for isolation.
- **[ASM-002]** Monetary transactions and account freezes are directed to a local simulated action service with SQLite audit log.
- **[ASM-003]** MCP servers operate over stdio and HTTP (JSON-RPC).
