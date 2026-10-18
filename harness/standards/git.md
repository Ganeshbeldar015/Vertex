# Git Standards & Workflow

> Specifies commit message conventions, branching rules, and parallel worktree isolation.

## 1. Commit Message Convention
Follow Conventional Commits: `<type>(<scope>): <short description>`
- `feat`: New functional capability
- `fix`: Bug fix
- `test`: Adding or modifying tests
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `chore`: Tooling, harness, dependencies, or configuration changes
- `docs`: Documentation updates

Examples:
- `chore(harness): scaffold sprint 0 infrastructure`
- `feat(graph): implement Louvain community detection MCP tool`
- `test(agent): add test for 4-hop circular flow detection`

## 2. Branching & Parallel Lanes
- Main development branch: `main`.
- Parallel Builder lanes utilize dedicated branches or git worktrees:
  `lane/<TASK-ID>-<lane-name>` (e.g. `lane/T-0001-graph`, `lane/T-0001-ui`).
- No two lanes may concurrently edit the same files (enforced by `harness/state/locks/` and `scripts/guard_paths.py`).
- Never force push (`push --force`) or hard reset against remote origin (`reset --hard origin`).
