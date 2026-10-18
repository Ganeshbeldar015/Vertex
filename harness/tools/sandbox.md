# Sandbox Execution Rules

> Defines the boundary conditions and safety constraints for bash and code execution within the harness.

## 1. Directory Boundaries
- All command execution must take place inside the repository root (`.`) or temporary build directories (`./tmp`, `./build`).
- Commands may never access or mutate user home directories (`~`), system directories (`/etc`, `C:\Windows`), or neighboring project workspaces.

## 2. Command Allow-list
- Only commands explicitly declared in `docs/harness.md` Section 8 are permitted for build and test tasks:
  - `python scripts/check_harness.py`
  - `pytest tests/harness`
  - `pytest tests/unit`
  - `pytest tests/integration`
  - `flake8 src tests`
  - `black --check src tests`
  - `mypy src tests`
  - `npm --prefix web ...`
- Read-only inspection commands are permitted: `ls`, `dir`, `cat`, `grep`, `rg`, `git status`, `git diff`, `git log`.

## 3. Network & Security Isolation
- No arbitrary network downloads or `curl | sh` scripts.
- Only official package registries (PyPI, npm) and authorized MCP endpoints are allow-listed.
- Never run with elevated administrator / root (`sudo`) privileges.
- Secret redaction: environment tokens matching `*_KEY`, `*_TOKEN`, `*_SECRET`, `ghp_*`, `sk-*` must never be output to terminal logs or committed files.

## 4. Execution Limits & Logging
- Default per-command timeout: 120 seconds.
- Per-stage tool call cap: governed by `harness/state/budgets.json`.
- Every command invocation and its exit code must be recorded in `harness/logs/events.jsonl`.
