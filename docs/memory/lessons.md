# Lessons Learned (Semantic Memory)

> Distilled rules, bug causes, and prevention policies. Format: `[L-NNN] Symptom -> Cause -> Rule`.

- **[L-001]** Windows command execution path separator issues -> Command line scripts often fail on backslash vs forward slash -> Always normalize file paths with POSIX forward slashes in tooling scripts.
- **[L-002]** Query injection vulnerabilities in dynamic Cypher queries -> Raw string formatting bypasses query planner safety -> All OpenCypher queries must use parameter maps ($param) and pass mcpcheck P-01...P-10.
- **[L-003]** In-memory property graph for rapid CI -> External database daemons cause flaky local test setups -> An in-memory property graph with OpenCypher parameter parsing enables sub-second (< 0.1s) hermetic unit tests.
- **[L-004]** Automated citation verification -> LLMs can hallucinate non-existent accounts -> Extracting entity tokens from rationales and asserting set containment against observed tool subgraphs provides 100% deterministic faithfulness.
- **[L-005]** Label propagation for fraud communities -> Fast iterative label propagation reliably clusters accounts sharing devices and transaction corridors without requiring external graph libraries.
- **[L-006]** Canonical cycle representations -> DFS cycle detection can report cyclic permutations of the same loop -> Canonicalizing cycles by rotating to the minimum node ID prevents duplicate findings.
