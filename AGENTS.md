# AGENTS.md — GraphSleuth (SENGRA)
> Map, not manual. Deep detail lives in linked files.

## What this is
Graph-Driven Investigation Agent detecting financial fraud rings via multi-hop graph reasoning and MCP tool selection. Single source of truth is [docs/harness.md](docs/harness.md).

## Start here (every session)
1. Read this file -> 2. [harness/state/state.json](harness/state/state.json) -> 3. [docs/prompt.md](docs/prompt.md) Boot Sequence (§1).

## Commands
- Install: `pip install -e ".[dev]" && npm --prefix web install`
- Lint: `flake8 src tests && npm --prefix web run lint`
- Format: `black --check src tests && prettier --check "web/**/*.{ts,tsx}"`
- Typecheck: `mypy src tests && npm --prefix web run type-check`
- Unit Test: `pytest tests/unit`
- Integration: `pytest tests/integration`
- Build: `npm --prefix web run build`
- Harness Check: `python scripts/check_harness.py && pytest tests/harness`

## Layout
- `AGENTS.md`: Top-level index map.
- `docs/`: Master prompt, raw problem statement, harness spec, MCP guides, memory, and ADRs.
- `harness/`: Profile, agents, roles, standards, workflows, tools registry, state, tasks, and logs.
- `scripts/`: Linter (`check_harness.py`), path guard (`guard_paths.py`), and breaker (`breaker.py`).
- `src/`: Product implementation (graph engine, MCP server, agent loop, actions, data generator, API).
- `web/`: Next.js analyst UI (alert queue, Cytoscape canvas, timeline, approvals).
- `tests/`: Harness self-tests, unit tests, and integration suites.

## Roles
| Agent | Role File | Primary Artifact |
|---|---|---|
| Orchestrator | [harness/roles/orchestrator.md](harness/roles/orchestrator.md) | `harness/state/state.json` |
| PO-Spec | [harness/roles/po-spec.md](harness/roles/po-spec.md) | `01-spec.md` |
| Designer | [harness/roles/designer.md](harness/roles/designer.md) | `02-design.md` |
| Tech Lead | [harness/roles/tech-lead.md](harness/roles/tech-lead.md) | `03-plan.md` |
| Test Author | [harness/roles/test-author.md](harness/roles/test-author.md) | `04-tests.md` |
| Builder | [harness/roles/builder.md](harness/roles/builder.md) | `05-build-<lane>.md` |
| Reviewer | [harness/roles/reviewer.md](harness/roles/reviewer.md) | `06-review.md` |
| Security | [harness/roles/security.md](harness/roles/security.md) | `06b-security.md` |
| QA | [harness/roles/qa.md](harness/roles/qa.md) | `07-qa.md` |
| Scribe | [harness/roles/scribe.md](harness/roles/scribe.md) | `08-docs.md` |
| Librarian | [harness/roles/librarian.md](harness/roles/librarian.md) | `docs/memory/lessons.md` |

## Rules (top 10)
1. **Never improvise outside the harness** — follow [docs/prompt.md](docs/prompt.md).
2. **Skinny agents, fat roles** — agents are <= 40 line pointers; logic lives in role files.
3. **Artifacts are the contract** — emit valid artifacts and [harness/standards/handoff-contract.md](harness/standards/handoff-contract.md).
4. **Nothing is done until checks pass** — strictly enforce [harness/standards/definition-of-done.md](harness/standards/definition-of-done.md).
5. **State lives on disk** — re-derive context from [harness/state/state.json](harness/state/state.json).
6. **Zero query injection** — all Cypher queries MUST use parameter maps per [harness/standards/coding.md](harness/standards/coding.md).
7. **Test-first discipline** — Red test runs precede implementation per [harness/standards/testing.md](harness/standards/testing.md).
8. **Stay in lane** — respect file locks and [harness/standards/git.md](harness/standards/git.md).
9. **Sandbox obedience** — execute only allow-listed commands per [harness/tools/sandbox.md](harness/tools/sandbox.md).
10. **Explainability faithfulness** — 100% of cited evidence IDs must map to real tool outputs.

## Gates & breakers
- Quality gates G0 (Integrity), G1 (Lane), G2 (Merge), G3 (Review), G4 (QA), G5 (Sprint). See [docs/prompt.md](docs/prompt.md) §9.
- Circuit breakers trip on repeated failures, guard violations, or budget exhaustion.

## Memory map
- Decisions: [harness/logs/decisions.log.md](harness/logs/decisions.log.md)
- Lessons learned: [docs/memory/lessons.md](docs/memory/lessons.md)
- Assumptions: [docs/memory/assumptions.md](docs/memory/assumptions.md)
- Failure records: [harness/logs/failures.log.md](harness/logs/failures.log.md)

## Do-not list
- Forbidden: editing files outside your role's allow-list; direct production DB writes without confirmation.
- Forbidden: deleting, disabling, or swallowing tests/lint warnings; committing hardcoded secrets.
