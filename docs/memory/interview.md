# Interview Log

> Verbatim record of discovery questions, problem statements, and requirements derived from raw.md.

## Q&A Summary
- **Problem Statement:** Build an agent that investigates financial fraud rings over connected data graphs, reasons across 2–6 hops, chooses tools via MCP, and produces explainable evidence subgraphs.
- **Primary Domain:** Financial fraud ring investigation (mule accounts, shared devices, circular money flows).
- **Tooling Protocol:** Model Context Protocol (MCP) using Python MCP SDK and `@falkordb/mcpserver`.
- **Target Verification:** 100% faithful explanations; zero unparameterized Cypher queries; deterministic test pyramid.
