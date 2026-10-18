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

### 3. Architecture
- **Data Generator:** Seeds realistic accounts, devices, and transactions with known fraud rings.
- **Graph Engine:** OpenCypher-compatible property graph with parameterized query execution.
- **MCP Server:** Exposes `graph.*` tools following JSON-RPC specifications.
- **Agent Loop:** Autonomous investigator executing hypothesis formulation, neighborhood expansion, and citation verification.
