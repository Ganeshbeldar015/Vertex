---
status: complete
owner: test-author
task: T-0003
acceptance_refs:
  - AC-003-a
  - AC-003-b
  - AC-003-c
  - AC-003-d
  - AC-003-e
---

# 04-Tests: Reasoning & Actions Red Test Suite

## 1. Acceptance Criteria to Test Matrix

| AC ID | Test Function | Test File | Target Module |
|---|---|---|---|
| **AC-003-a** | `test_score_risk_computes_factor_breakdown` | `tests/unit/test_reasoning_and_actions.py` | `src.graph.risk.compute_risk_score` |
| **AC-003-b** | `test_agent_hypothesis_loop_investigates_ring` | `tests/unit/test_reasoning_and_actions.py` | `src.agent.loop.InvestigationAgent` |
| **AC-003-c** | `test_action_service_queues_gated_freeze` | `tests/unit/test_reasoning_and_actions.py` | `src.actions.service.ActionService` |
| **AC-003-d** | `test_action_approval_and_reversibility` | `tests/unit/test_reasoning_and_actions.py` | `src.actions.service.ActionService` |
| **AC-003-e** | `test_action_log_maintains_immutable_audit` | `tests/unit/test_reasoning_and_actions.py` | `src.actions.service.ActionService` |
| **Contract** | `test_mcp_action_tool_dispatch` | `tests/unit/test_reasoning_and_actions.py` | `src.mcp.server.SengraMCPServer` |

## 2. Red Test Run Evidence

```
$ python -m pytest tests/unit/test_reasoning_and_actions.py
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1
collected 0 items / 1 error

=================================== ERRORS ====================================
ERROR collecting tests/unit/test_reasoning_and_actions.py
E   ModuleNotFoundError: No module named 'src.graph.risk'
============================== 1 error in 0.23s ===============================
Exit Code: 1 (Failing - Red)
```

## 3. Test Determinism & Constraints
- Hermetic test fixture `fraud_setup`.
- Zero live external network connections.
- Sub-second execution (< 0.2s).
