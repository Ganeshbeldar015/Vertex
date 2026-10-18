# Testing Standards

> Specifies test organization, pyramid layers, determinism, and coverage thresholds.

## 1. Test Pyramid
- **Unit Tests (`tests/unit/`):** Fast (< 1s per test), hermetic, no live network calls. Tests isolate graph algorithms, query generation, risk scoring formulas, and citation verification.
- **Integration Tests (`tests/integration/`):** Test end-to-end multi-hop queries, MCP server tool dispatch, and simulated action services against disposable test graph fixtures.
- **Harness Self-Tests (`tests/harness/`):** Deterministic unit tests validating `check_harness.py`, `guard_paths.py`, and `breaker.py`.

## 2. Test-First Discipline (Red -> Green)
- Acceptance criteria (AC-xxx-y) are converted into failing unit tests by Test Author before Builder writes implementation code.
- Red test runs are captured with exit code and failure logs in `harness/artifacts/<TASK-ID>/04-tests.md`.

## 3. Coverage & Quality Floors
- Minimum 80% line coverage on changed lines for all pull requests.
- Forbidden cheats: No deleting or weakening existing tests, no skipping tests (`@pytest.mark.skip`, `xfail`) to achieve green status.
- Flaky tests are quarantined in `docs/memory/lessons.md` and fixed promptly; never retry-until-green.
