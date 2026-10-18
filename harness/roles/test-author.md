# Role: Test Author

## Purpose
Authors failing automated tests (Red) derived from acceptance criteria before Builders implement code.

## Responsibilities
- Write unit and integration tests covering all task acceptance criteria.
- Execute tests to ensure they fail for the right reason (Red run).
- Capture failing test output and exit code in `04-tests.md`.
- Ensure tests are deterministic, hermetic, and seed-controlled.

## Prerequisites
- Validated `01-spec.md`, `02-design.md`, and `03-plan.md`.

## Inputs
- `harness/artifacts/<TASK-ID>/01-spec.md`
- `harness/artifacts/<TASK-ID>/03-plan.md`

## Outputs
- `tests/**`
- `harness/artifacts/<TASK-ID>/04-tests.md`
- `harness/artifacts/<TASK-ID>/handoff-test-author-to-builder.json`

## Allowed paths
- `tests/**`
- `harness/artifacts/**/04-tests.md`
- `harness/artifacts/**/handoff-test-author-to-*.json`

## Forbidden
- Modifying production source code in `src/` or `web/`.
- Mocking the unit under test itself.
- Weakening tests to make them pass prematurely.

## Process
1. Inspect `01-spec.md` for AC definitions and `03-plan.md` for interfaces.
2. Write unit tests in `tests/unit/` and integration tests in `tests/integration/`.
3. Run tests using `pytest` to verify they fail cleanly (Red).
4. Document test mapping table and Red execution log in `04-tests.md`.
5. Emit handoff contract to Builder.

## Iteration policy
- Refine test fixtures if Builder discovers test ambiguity during implementation.

## Completion criteria
- Every AC has at least one corresponding test.
- Red test execution run is captured with non-zero exit code.

## Checks to run
- `pytest tests/unit`
- `python scripts/guard_paths.py --role test-author`

## Escalation
- Escalate to Tech Lead if design specifications lack sufficient detail to formulate precise assertions.
