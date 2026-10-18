# Parallel Lanes & Isolation Model

> Guidelines for managing concurrent Builder lanes without merge conflicts or state corruption.

## 1. Lane Principles
1. **Exclusive File Ownership:** No two Builder lanes may touch or modify the same file concurrently. The Tech Lead declares file ownership in `03-plan.md`, recorded in `harness/state/locks/<lane>.json`.
2. **Branch Isolation:** Each lane operates on a dedicated branch: `lane/<TASK-ID>-<lane-name>`.
3. **Pre-Merge Validation:** Before merging into the integration branch, each lane must pass Gate G1 (lint, typecheck, lane unit tests) in isolation.
4. **Concurrency Ceiling:** Governed by `max_parallel_agents` in `harness/state/budgets.json` (default: 3).
