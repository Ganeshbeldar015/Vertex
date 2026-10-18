# Sprint Template & Ceremonies

> Standard operating procedure for sprint planning, execution, demo, and retrospective.

## 1. Sprint Lifecycle
1. **Planning:**
   - Select backlog items from `harness/backlog.md` according to MoSCoW priorities.
   - Elaborate task definitions into `harness/tasks/<TASK-ID>.md`.
   - Initialize task artifact skeletons in `harness/artifacts/<TASK-ID>/`.
   - Update `harness/state/state.json`.

2. **Execution:**
   - Execute the stage pipeline for each task.
   - Run parallel lanes in separate branches or worktrees.
   - Enforce gates G0 through G4 on every task.

3. **Sprint Review & Demo:**
   - Demonstrate the walking skeleton or feature increment against acceptance criteria.
   - Capture user feedback and sign-off in `harness/logs/decisions.log.md`.

4. **Retrospective (Retro):**
   - Review failed gates, breaker trips, and retry metrics in `harness/logs/failures.log.md`.
   - Extract actionable insights into `docs/memory/lessons.md`.
   - Tighten harness standards, scripts, or role prompts if needed.
