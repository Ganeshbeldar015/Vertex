---
status: complete
owner: test-author
task: T-0001
acceptance_refs:
  - AC-001-a
  - AC-002-a
  - AC-003-a
  - AC-004-a
  - AC-005-a
---

# 04-Tests: Walking Skeleton Red Test Suite

## 1. Acceptance Criteria to Test Matrix

| AC ID | Test Function | Test File | Target Module |
|---|---|---|---|
| **AC-001-a** | `test_synthetic_generator_creates_hero_ring` | `tests/unit/test_walking_skeleton.py` | `src.data.generator` |
| **AC-002-a** | `test_graph_engine_parameterized_query` | `tests/unit/test_walking_skeleton.py` | `src.graph.engine` |
| **AC-003-a** | `test_mcp_tool_dispatch` | `tests/unit/test_walking_skeleton.py` | `src.mcp.server` |
| **AC-004-a** | `test_agent_investigation_finds_ring` | `tests/unit/test_walking_skeleton.py` | `src.agent.loop` |
| **AC-005-a** | `test_citation_verifier_validates_evidence` | `tests/unit/test_walking_skeleton.py` | `src.agent.verifier` |

## 2. Red Test Run Evidence

```
$ python -m pytest tests/unit/test_walking_skeleton.py
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1
collected 0 items / 1 error

=================================== ERRORS ====================================
ERROR collecting tests/unit/test_walking_skeleton.py
E   ModuleNotFoundError: No module named 'src'
============================== 1 error in 0.46s ===============================
Exit Code: 1 (Failing - Red)
```

## 3. Test Determinism & Constraints
- No external network access or live cloud services.
- Randomness seeded at `seed=42`.
- Fast hermetic execution (< 1s per test).
