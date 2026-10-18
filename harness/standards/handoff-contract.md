# Handoff Contract Specification

> Every inter-role transition must emit a validated handoff JSON in `harness/artifacts/<TASK-ID>/handoff-<from>-to-<to>.json`.

## 1. Schema Definition

```json
{
  "task_id": "T-0001",
  "from": "tech-lead",
  "to": "test-author",
  "artifact": "harness/artifacts/T-0001/03-plan.md",
  "status": "complete",
  "summary": "Implementation plan decomposed into 2 lanes: graph-core and agent-loop.",
  "inputs_consumed": ["01-spec.md", "02-design.md"],
  "acceptance_refs": ["AC-001-a", "AC-002-a"],
  "open_questions": [],
  "assumptions": [],
  "files_touched": ["harness/artifacts/T-0001/03-plan.md"],
  "checks_run": [{"cmd": "python scripts/guard_paths.py --role tech-lead", "exit": 0}],
  "next_expected_artifact": "04-tests.md"
}
```

## 2. Validation & Rejection Criteria
The Orchestrator automatically rejects a handoff and halts the pipeline if:
1. The declared `artifact` file does not exist on disk.
2. `status` is not `complete` (e.g. `blocked` or `needs-info`).
3. An ID in `acceptance_refs` is not defined in `docs/harness.md`.
4. Any path in `files_touched` is outside the emitting role's allow-list.
5. `checks_run` is empty for roles with mandatory checks (Builder, Test Author, Reviewer).
6. Summary exceeds 120 words.
