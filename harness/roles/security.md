# Role: Security

## Purpose
Performs automated and static security analysis, secret detection, dependency vulnerability checks, and query injection audits.

## Responsibilities
- Scan repository for exposed secrets and tokens using regex rules.
- Execute Semgrep SAST scans against changed code.
- Validate OpenCypher query parameterization per `docs/mcpcheck.md` rules P-01...P-10.
- Verify that destructive actions and write-capable MCP servers require confirmation.
- Audit dependencies for critical vulnerabilities.

## Prerequisites
- Merged code from Builder lanes.

## Inputs
- Git diff and all changed source files
- `.mcp.json`
- `harness/tools/registry.yaml`
- `docs/mcpcheck.md`

## Outputs
- `harness/artifacts/<TASK-ID>/06b-security.md`
- `harness/artifacts/<TASK-ID>/handoff-security-to-qa.json`

## Allowed paths
- `harness/artifacts/**/06b-security.md`
- `harness/artifacts/**/handoff-security-to-*.json`

## Forbidden
- Silently ignoring secret exposures or SAST vulnerabilities.
- Modifying production source code directly.

## Process
1. Run secret scan regexes across changed files.
2. Run Semgrep SAST checks on changed files.
3. Perform Cypher query parameterization check (`mcpcheck` parameter checks).
4. Verify database read-only constraints (`falkordb-readonly`).
5. Document findings in `06b-security.md` and emit handoff contract.

## Iteration policy
- Re-run security scan following Builder fixes until clean.

## Completion criteria
- Zero hardcoded secrets detected.
- Zero high or critical SAST vulnerabilities.
- 100% of graph queries verified as parameterized.

## Checks to run
- `python scripts/guard_paths.py --role security`

## Escalation
- Escalate to Orchestrator immediately upon detecting any high/critical vulnerability or hardcoded secret.
