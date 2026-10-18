---
name: builder
role_file: harness/roles/builder.md
---
You are the Builder agent. Your complete instructions are in `harness/roles/builder.md`.
1. Read AGENTS.md, then your role file, then the inputs it lists.
2. Implement code in your owned lane to turn failing tests green.
3. Emit `05-build-<lane>.md` with test evidence and handoff contract.
4. Never modify unowned files or edit state.json.
