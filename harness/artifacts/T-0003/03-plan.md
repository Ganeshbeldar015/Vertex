---
status: complete
owner: tech-lead
task: T-0003
acceptance_refs:
  - AC-003-a
  - AC-003-b
  - AC-003-c
  - AC-003-d
  - AC-003-e
---

# 03-Plan: Multi-Hop Reasoning & Action Layer Implementation Plan

## 1. Technical Strategy
Build modular components for composite risk analytics, action lifecycle management, and agent hypothesis evaluation.
- `src/graph/risk.py`: Encapsulates multi-feature graph heuristic calculation (shared device, circular flow, community density, velocity).
- `src/actions/service.py`: Encapsulates simulated core banking, case tracking, approval state machine (`PENDING_APPROVAL` -> `APPROVED` / `REJECTED`), reversibility, and immutable `ActionLog`.
- `src/agent/loop.py`: Enriches investigation loop to test explicit hypotheses across 3 hops, score risk, and execute decision policy actions.
- `src/mcp/server.py`: Adds `algo.score_risk` and `action.*` dispatchers.

## 2. File-Level Decomposition
1. `src/graph/risk.py`:
   - `compute_risk_score(graph, account_id) -> dict`: Evaluates 4 factors, sums weighted scores, determines risk tier (`LOW`, `MEDIUM`, `HIGH`).
2. `src/actions/__init__.py` & `src/actions/service.py`:
   - `ActionService` class:
     - `create_case(title, entity_ids, summary)`
     - `flag_entity(case_id, entity_id, reason, evidence_ids)`
     - `freeze_account(case_id, account_id, reason, evidence_ids, auto_exec=False)`
     - `block_device(case_id, device_id, reason, evidence_ids)`
     - `approve_action(action_id, approver_id)`
     - `reverse_action(action_id, reason, approver_id)`
     - `get_action_log(case_id=None)`
3. `src/agent/loop.py`:
   - Enhance `InvestigationAgent`:
     - Run `algo.detect_communities` and `algo.detect_cycles`.
     - Run `algo.score_risk`.
     - Apply decision policy: if risk > 0.70, create case, auto-flag ring entities, queue freeze on suspect accounts, queue device block on shared devices.
4. `src/mcp/server.py`:
   - Connect `ActionService` to `SengraMCPServer` and register tools.

## 3. Lane Allocation & Ownership
- **Lane `main`:**
  - Owner: `builder`
  - Owned paths: `src/graph/**`, `src/actions/**`, `src/agent/**`, `src/mcp/**`
  - Lock recorded in: `harness/state/locks/main.json`

## 4. Test Strategy per AC
- **AC-003-a:** `test_score_risk_computes_factor_breakdown` tests multi-factor scoring on `A-1042`.
- **AC-003-b:** `test_agent_hypothesis_loop_investigates_ring` tests multi-hop hypothesis testing within 15 calls.
- **AC-003-c:** `test_action_service_queues_gated_freeze` tests action entry into `PENDING_APPROVAL`.
- **AC-003-d:** `test_action_approval_and_reversibility` tests approval execution and unfreeze reversal.
- **AC-003-e:** `test_action_log_maintains_immutable_audit` tests action log persistence and idempotency.
