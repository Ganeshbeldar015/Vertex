# Definition of Done (Global Quality Gates)

> A task or sprint is strictly Done only when all of the following conditions are deterministically verified.

## 1. Task Definition of Done
- [ ] **Artifacts complete:** All stage artifacts `01` through `08` exist under `harness/artifacts/<TASK-ID>/`.
- [ ] **Handoffs validated:** Every inter-role handoff has a valid JSON contract with zero schema violations.
- [ ] **Gate G0 (Harness integrity):** `python scripts/check_harness.py` exits 0 and all harness unit tests pass.
- [ ] **Gate G1 (Lane verification):** Format, lint, typecheck, and unit tests for the lane pass with exit code 0.
- [ ] **Gate G2 (Merge verification):** Full test suite passes; test coverage on changed lines >= 80%.
- [ ] **Gate G3 (Review & Security):** Zero BLOCKER or MAJOR review findings; Semgrep SAST clean; zero hardcoded secrets.
- [ ] **Gate G4 (QA & Acceptance):** Integration tests pass; 100% of acceptance criteria (AC-xxx-y) have passing test evidence; citation verifier reports 0 unverified claims.
- [ ] **Guards & Breakers:** No path guard violations; no circuit breaker tripped; no unresolved open questions.
- [ ] **Audit & Memory:** `state.json`, `events.jsonl`, and `docs/memory/lessons.md` are updated.

## 2. Sprint Definition of Done
- [ ] All tasks planned for the sprint have achieved Task DoD.
- [ ] Gate G5 Sprint demo completed and ratified by user sign-off.
- [ ] Sprint retrospective completed: Librarian proposed learnings captured in `docs/memory/lessons.md`.
