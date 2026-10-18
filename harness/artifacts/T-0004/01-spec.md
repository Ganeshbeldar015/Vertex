---
status: complete
owner: po-spec
task: T-0004
acceptance_refs:
  - AC-009-a
  - AC-010-a
---

# 01-Spec: Explainability & Analyst Web UI

## 1. Intent & Problem Summary
Deliver an end-to-end explainability and visual investigation interface for GraphSleuth. Fraud analysts require an intuitive, real-time interface to inspect incoming alerts, trigger multi-hop investigations, observe the agent's live reasoning timeline, explore the evidence subgraph in an interactive canvas with highlighted rings, and review or execute gated remediation actions (account freezes, device blocks) with an exportable audit report.

## 2. Scope Boundaries
- **In Scope:**
  - REST API in `src/api/server.py` exposing:
    - `GET /api/alerts`: Alert queue with severity, entity target, and investigation status.
    - `POST /api/investigate`: Runs autonomous multi-hop investigation and returns structured case summary, timeline, and Cytoscape subgraph.
    - `GET /api/cases/{case_id}`: Retrieves full case details with timeline and evidence.
    - `GET /api/actions`: Lists pending and executed actions.
    - `POST /api/actions/{action_id}/approve`: Approves a pending action.
    - `POST /api/actions/{action_id}/reject`: Rejects a pending action.
    - `POST /api/actions/{action_id}/reverse`: Reverses an executed action.
    - `GET /api/cases/{case_id}/export`: Exports a structured Markdown case report.
  - Citation verification engine (`src/agent/verifier.py`): Ensures 100% of cited entity/transaction IDs in narrative rationales correspond to observed tool evidence.
  - Next.js / React Analyst UI in `web/`:
    - Alert Queue component with status filters and one-click investigation trigger.
    - Cytoscape canvas visualizing evidence subgraphs with colored node types (Account, Device, Customer) and highlighted fraud rings.
    - Live Agent Timeline visualizing hypotheses, tool calls, and observations.
    - Action Approval Panel with 1-click Approve / Reject buttons and audit log.
    - Case Report Export modal.
- **Out of Scope:**
  - Automated ground-truth benchmark evaluation against public datasets (Sprint 5).

## 3. User Stories
- **US-4.1 (Verifiable Rationale):** As a fraud analyst, I want the agent's narrative report to cite specific entity IDs and transaction amounts so that every claim is 100% verifiable against the graph.
- **US-4.2 (Interactive Evidence Canvas):** As an analyst, I want to visually inspect the multi-hop fraud cluster in a force-directed graph canvas that clearly highlights shared devices and circular flows.
- **US-4.3 (Live Agent Timeline):** As an analyst, I want to observe each tool call made by the agent during investigation to understand how it reached its conclusions.
- **US-4.4 (One-Click Action Approval):** As a risk lead, I want to review pending account freeze and device block requests with attached evidence and approve them with one click.
- **US-4.5 (Audit Report Export):** As a compliance officer, I want to export an investigation report in Markdown containing findings, evidence lists, and action history.

## 4. Requirement to Acceptance Mapping

| Requirement | Acceptance ID | Given / When / Then Specification |
|---|---|---|
| **REQ-013** (Explanation Faithfulness) | **AC-009-a** | **Given** an investigation narrative on account `A-1042`, **When** the citation verifier validates the report, **Then** 100% of cited entity and transaction IDs map to real observed tool outputs (0 unverified citations). |
| **REQ-014** (Analyst UI Visualization & API) | **AC-010-a** | **Given** the Analyst UI and API, **When** inspecting an active investigation, **Then** the Cytoscape graph canvas renders the evidence subgraph with highlighted fraud rings, the alert queue displays prioritized alerts, the agent timeline traces tool calls, and the approval panel enables 1-click action approvals. |

## 5. Edge Cases & Performance
- Canvas Performance: Subgraphs with up to 50 nodes and 100 edges must render in under 2 seconds.
- Missing Case ID: API requests to nonexistent cases return HTTP 404 with standard error format.
- Unauthorized Approvals: Action approval requests without an approver name are rejected with HTTP 400.
