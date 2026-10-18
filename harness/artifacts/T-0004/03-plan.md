---
status: complete
owner: tech-lead
task: T-0004
acceptance_refs:
  - AC-009-a
  - AC-010-a
---

# 03-Plan: Explainability & Analyst UI Implementation Plan

## 1. Lane Breakdown

### Lane 1: API Core (`src/api/`)
- **Owner:** Builder (API Lane)
- **Files:** `src/api/__init__.py`, `src/api/server.py`, `src/api/formatters.py`
- **Deliverables:**
  - FastAPI application with CORS and JSON responses.
  - In-memory alert registry pre-populated with hero scenario alerts (`ALT-1001` on `A-1042`).
  - `/api/investigate` endpoint running `InvestigationAgent` and returning Cytoscape elements.
  - Cytoscape formatter converting nodes/edges into `{data: {id, label, type, risk_score, is_ring}}`.
  - Case report exporter generating structured Markdown reports.
  - Action endpoints for approval, rejection, and reversal connected to `ActionService`.

### Lane 2: Web UI (`web/`)
- **Owner:** Builder (Web Lane)
- **Files:** `web/package.json`, `web/src/components/*`, `web/src/pages/index.tsx` (or standalone SPA bundle)
- **Deliverables:**
  - Modern Next.js / React application with Cytoscape.js canvas.
  - Alert Queue, Cytoscape Canvas, Agent Timeline, and Action Approval Panel.
  - Quick-start dev and build scripts (`npm --prefix web run build`).

### Lane 3: Automated Verification
- **Owner:** Test Author
- **Files:** `tests/unit/test_api_and_ui.py`
- **Deliverables:**
  - Red tests checking all API endpoints via `fastapi.testclient.TestClient`.
  - Test verifying Cytoscape element serialization and ring tagging.
  - Test verifying 100% citation faithfulness in case rationale.
  - Test verifying 1-click action approval and reversal flow.

## 2. Gate Criteria & Constraints
- Diff limit: < 400 lines per module.
- Test execution time: < 1.0s for full API and serialization suite.
- Security: CORS configured safely; input validation on all path parameters.
