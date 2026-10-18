# Lessons Learned (Semantic Memory)

> Distilled rules, bug causes, and prevention policies. Format: `[L-NNN] Symptom -> Cause -> Rule`.

- **[L-001]** Windows command execution path separator issues -> Command line scripts often fail on backslash vs forward slash -> Always normalize file paths with POSIX forward slashes in tooling scripts.
- **[L-002]** Query injection vulnerabilities in dynamic Cypher queries -> Raw string formatting bypasses query planner safety -> All OpenCypher queries must use parameter maps ($param) and pass mcpcheck P-01...P-10.
- **[L-003]** In-memory property graph for rapid CI -> External database daemons cause flaky local test setups -> An in-memory property graph with OpenCypher parameter parsing enables sub-second (< 0.1s) hermetic unit tests.
- **[L-004]** Automated citation verification -> LLMs can hallucinate non-existent accounts -> Extracting entity tokens from rationales and asserting set containment against observed tool subgraphs provides 100% deterministic faithfulness.
- **[L-005]** Label propagation for fraud communities -> Fast iterative label propagation reliably clusters accounts sharing devices and transaction corridors without requiring external graph libraries.
- **[L-006]** Canonical cycle representations -> DFS cycle detection can report cyclic permutations of the same loop -> Canonicalizing cycles by rotating to the minimum node ID prevents duplicate findings.
- **[L-007]** Descriptive commit messages -> Avoid meta terms like 'harness' or 'walking skeleton' -> Write commit messages describing the actual code, features, or files added and modified.
- **[L-008]** High-impact actions and blast radius -> Uncontrolled autonomous agent actions can trigger false-positive account freezes -> Enforce a strict state machine where high-impact actions enter PENDING_APPROVAL, require human signoff, and support deterministic reversal (unfreeze).
- **[L-009]** Multi-factor risk scoring calibration -> Single graph metrics produce noisy false positives -> Weight multiple independent topology signals (shared devices 35%, circular flows 30%, community density 20%, velocity 15%) for robust fraud identification.
- **[L-010]** Cytoscape data serialization -> Graph nodes and edges have heterogeneous property types -> Formatting nodes with explicit type tags and boolean is_ring flags allows unified CSS styling and highlighting in Cytoscape.js.
- **[L-011]** Next.js static build in monorepo setup -> Missing .eslintrc.json prompts interactively in CI environments -> Always provide an explicit .eslintrc.json configuration to ensure headless non-interactive builds succeed.
- **[L-012]** Ground-truth benchmark partitioning -> Evaluating on single rings can mask detection weaknesses on other topological structures -> Include multiple distinct topologies (shared devices, hub routing, circular flows) and negative decoy controls to validate generalizability.
- **[L-013]** Blast-radius limits on automated actions -> Autonomous agents can trigger cascade account freezes on large suspected clusters -> Enforce a strict pre-execution cap (<= 10 freezes per case) to prevent accidental mass operational disruption.
