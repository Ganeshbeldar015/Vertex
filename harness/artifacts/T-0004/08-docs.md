---
status: complete
owner: scribe
task: T-0004
acceptance_refs:
  - AC-009-a
  - AC-010-a
---

# 08-Docs: Explainability & Analyst UI Documentation

## 1. Documentation Updates
- Updated `CHANGELOG.md` with version `[0.4.0] - 2026-10-18`.
- Updated `README.md` with instructions on running the FastAPI backend server and Next.js Analyst UI.
- Documented REST API endpoints:
  - `GET /api/alerts`: Returns incoming prioritized fraud alerts.
  - `POST /api/investigate`: Runs autonomous multi-hop investigation on target account.
  - `GET /api/cases/{case_id}`: Retrieves case results with Cytoscape elements.
  - `GET /api/cases/{case_id}/export`: Exports auditor-ready Markdown report.
  - `GET /api/actions`: Retrieves audit log of remediation actions.
  - `POST /api/actions/{action_id}/approve`: Approves a pending action.
  - `POST /api/actions/{action_id}/reject`: Rejects a pending action.
  - `POST /api/actions/{action_id}/reverse`: Reverses an executed action.
- Documented Web UI components in `web/src/components/`:
  - `AlertQueue`: Interactive queue with severity badges.
  - `CytoscapeCanvas`: Force-directed graph canvas highlighting fraud rings and shared devices.
  - `AgentTimeline`: Live stepper displaying tool calls and hypothesis confirmations.
  - `ActionApprovalPanel`: 1-click Approve / Reject interface for gated remediation requests.
  - `CaseReportModal`: Case report viewer and Markdown exporter.
