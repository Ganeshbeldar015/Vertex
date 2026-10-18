# Git Standards & Workflow

> Specifies commit message conventions, branching rules, and parallel worktree isolation.

## 1. Commit Message Convention
Follow Conventional Commits: `<type>(<scope>): <descriptive summary of what changed>`
- Commit messages must directly describe the concrete functionality or files added/modified.
- Avoid abstract meta terms (such as "harness", "walking skeleton").
- Examples:
  - `feat(graph): implement Louvain community detection and PageRank centrality`
  - `feat(mcp): add cycle detection and shared attributes tools`
  - `feat(actions): add account freeze and device block approval service`
  - `test(algorithms): add tests for circular transfer loops`
  - `docs(readme): update setup commands and architecture overview`

## 2. Branching & Parallel Lanes
- Main development branch: `main`.
- Parallel Builder lanes utilize dedicated branches or git worktrees:
  `lane/<TASK-ID>-<lane-name>` (e.g. `lane/T-0001-graph`, `lane/T-0001-ui`).
- No two lanes may concurrently edit the same files (enforced by `harness/state/locks/` and `scripts/guard_paths.py`).
- Never force push (`push --force`) or hard reset against remote origin (`reset --hard origin`).
