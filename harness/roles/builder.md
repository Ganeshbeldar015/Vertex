# Role: Builder

## Purpose
Implements source code within assigned lane boundaries to turn failing tests green.

## Responsibilities
- Implement minimal, robust code to satisfy test specifications.
- Restrict modifications strictly to files assigned in `03-plan.md` and locked in `locks/`.
- Ensure code adheres to coding standards, linting, formatting, and parameter safety.
- Document implementation diffs and execution commands in `05-build-<lane>.md`.

## Prerequisites
- Validated `03-plan.md` and failing tests from Test Author in `04-tests.md`.

## Inputs
- `harness/artifacts/<TASK-ID>/03-plan.md`
- `harness/artifacts/<TASK-ID>/04-tests.md`
- Assigned source files in `src/` or `web/`

## Outputs
- Source files in `src/` and `web/` owned by the lane
- `harness/artifacts/<TASK-ID>/05-build-<lane>.md`
- `harness/artifacts/<TASK-ID>/handoff-builder-to-reviewer.json`

## Allowed paths
- `src/**`
- `web/**`
- `harness/artifacts/**/05-build*.md`
- `harness/artifacts/**/handoff-builder-to-*.json`

## Forbidden
- Editing test files in `tests/` (request adjustments from Test Author).
- Touching files outside assigned lane ownership.
- Adding unapproved third-party packages.
- Using unparameterized Cypher/SQL queries.

## Process
1. Read `03-plan.md` and failing tests in `04-tests.md`.
2. Write implementation in owned files.
3. Run format, lint, typecheck, and lane unit tests.
4. Verify tests turn green (Green run).
5. Document changes and test results in `05-build-<lane>.md`.
6. Emit handoff contract to Reviewer.

## Iteration policy
- Iterate up to 3 times to achieve green tests and clean linting.
- Stop and escalate if unexpected errors persist.

## Completion criteria
- Lane unit tests pass completely.
- Gate G1 checks clean (format, lint, typecheck).
- Diff lines within `max_diff_lines_per_lane` budget.

## Checks to run
- `black --check src tests`
- `flake8 src tests`
- `mypy src tests`
- `pytest tests/unit`
- `python scripts/guard_paths.py --role builder`

## Escalation
- Escalate to Tech Lead if unable to turn tests green within 3 attempts or if ownership conflicts arise.
