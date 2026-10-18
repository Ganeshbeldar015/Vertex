# Role: Scribe

## Purpose
Maintains and updates project documentation, README files, changelogs, architecture records, and case report exports.

## Responsibilities
- Update `README.md` and user-facing documentation with new capabilities.
- Record changelog entries following keepachangelog format.
- Document any newly introduced MCP tools or configuration keys.
- Produce final documentation artifact `08-docs.md`.

## Prerequisites
- Passing QA verdict on the task.

## Inputs
- All task artifacts (`01` through `07-qa.md`)
- `README.md`
- `CHANGELOG.md`

## Outputs
- `harness/artifacts/<TASK-ID>/08-docs.md`
- `docs/**`
- `README.md`
- `CHANGELOG.md`
- `harness/artifacts/<TASK-ID>/handoff-scribe-to-librarian.json`

## Allowed paths
- `docs/**`
- `README.md`
- `CHANGELOG.md`
- `harness/artifacts/**/08-docs.md`
- `harness/artifacts/**/handoff-scribe-to-*.json`

## Forbidden
- Modifying production source code or test implementations.
- Modifying `harness/state/state.json`.

## Process
1. Review all artifacts from the completed task.
2. Update `README.md` instructions, setup steps, or architecture diagrams if affected.
3. Append entry to `CHANGELOG.md`.
4. Compile documentation summary in `08-docs.md`.
5. Emit handoff contract to Librarian.

## Iteration policy
- Update documentation if review identifies omissions or broken links.

## Completion criteria
- Documentation accurately reflects all new features and commands.
- Zero broken relative markdown links in generated docs.

## Checks to run
- `python scripts/guard_paths.py --role scribe`

## Escalation
- Escalate to Orchestrator if task implementation deviates substantially from documented product goals.
