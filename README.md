# GraphSleuth (SENGRA)

> Graph-Driven Investigation Agent for Financial Fraud Ring Investigation.

## Overview
GraphSleuth is an AI agent that navigates a connected property graph across 2–6 hops, selects tools through the Model Context Protocol (MCP), detects complex financial fraud rings (such as shared device clusters and circular money laundering flows), and produces fully verifiable, cited evidence subgraphs.

## Quickstart

### 1. Requirements
- Python 3.14+
- Node.js v24+

### 2. Run Self-Tests & Verifications
```bash
# Verify harness integrity (Gate G0)
python scripts/check_harness.py
pytest tests/harness

# Run walking skeleton unit tests
pytest tests/unit
```

### 3. Run Application
```bash
# Start FastAPI backend API (port 8000)
python -m uvicorn src.api.server:create_app --factory --port 8000 --reload

# Start Next.js Analyst UI (port 3000)
npm --prefix web run dev
```

### 4. Architecture
- **Data Generator:** Seeds realistic accounts, devices, and transactions with known fraud rings.
- **Graph Engine:** OpenCypher-compatible property graph with parameterized query execution.
- **MCP Server:** Exposes `graph.*`, `algo.*`, and `action.*` tools following JSON-RPC specifications.
- **Agent Loop:** Autonomous investigator executing hypothesis formulation, neighborhood expansion, and citation verification.
- **Action Service:** Gated core banking actions with approval matrix, reversibility, and immutable audit logs.
- **Analyst Web UI:** Next.js application with Cytoscape canvas visualization, alert queue, timeline, and 1-click approvals.
