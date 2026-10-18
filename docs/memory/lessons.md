# Lessons Learned (Semantic Memory)

> Distilled rules, bug causes, and prevention policies. Format: `[L-NNN] Symptom -> Cause -> Rule`.

- **[L-001]** Windows command execution path separator issues -> Command line scripts often fail on backslash vs forward slash -> Always normalize file paths with POSIX forward slashes in tooling scripts.
- **[L-002]** Query injection vulnerabilities in dynamic Cypher queries -> Raw string formatting bypasses query planner safety -> All OpenCypher queries must use parameter maps ($param) and pass mcpcheck P-01...P-10.
