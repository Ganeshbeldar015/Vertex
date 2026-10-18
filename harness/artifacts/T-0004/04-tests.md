---
status: complete
owner: test-author
task: T-0004
acceptance_refs:
  - AC-009-a
  - AC-010-a
---

# 04-Tests: Explainability, API & UI Test Suite

## 1. Test Suite Structure
- Test file: `tests/unit/test_api_and_ui.py`
- Test Framework: `pytest` + `fastapi.testclient.TestClient`

## 2. Red Phase Verification
- **Command:** `python -m pytest tests/unit/test_api_and_ui.py`
- **Result:** FAILED (`ModuleNotFoundError: No module named 'src.api'`)
- **Status:** Red tests established cleanly before implementation.

## 3. Test Cases Implemented

| Test Function | Acceptance ID | Target Behavior Verified |
|---|---|---|
| `test_get_alerts_endpoint` | `AC-010-a` | `GET /api/alerts` returns list containing hero account `A-1042` with `HIGH`/`CRITICAL` severity. |
| `test_investigate_account_returns_cytoscape_and_timeline` | `AC-010-a` | `POST /api/investigate` triggers multi-hop reasoning, returns risk score >= 0.75, Cytoscape nodes/edges with `is_ring` highlights, and step timeline. |
| `test_case_export_markdown` | `AC-010-a` | `GET /api/cases/{case_id}/export` returns structured Markdown report for auditors with headers, risk score, citations, and timeline. |
| `test_action_approval_api_workflow` | `AC-010-a` | API endpoints allow fetching pending actions, approving an action to `COMPLETED`, and reversing to `REVERSED`. |
| `test_citation_faithfulness_verification` | `AC-009-a` | Narrative rationale evaluated with `verify_citations` produces 100% faithfulness score and 0 unsupported citations against observed graph nodes. |

## 4. Gate G1 Readiness
All test cases defined and ready for Builder to fulfill.
