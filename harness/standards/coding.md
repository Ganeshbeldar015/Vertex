# Coding Standards

> Defines code quality, formatting, language conventions, and security rules for GraphSleuth.

## 1. Python Standards
- Python 3.14+ compatibility.
- Style: Strict PEP 8 conformance formatted with `black --line-length 100`.
- Linting: `flake8 src tests` with zero warnings.
- Type Checking: `mypy src tests --strict` required.
- Parameterized Queries: All OpenCypher and SQL queries MUST use query parameters (e.g., `graph.query("MATCH (a:Account {id: $id}) RETURN a", {"id": acc_id})`). String interpolation (`f"..."`, `+`, `%`) in query strings is strictly forbidden and rejected at Gate G1.

## 2. TypeScript / React Standards
- TypeScript in strict mode (`"strict": true` in `tsconfig.json`).
- ESLint and Prettier formatting.
- Components use functional React patterns with hooks; shadcn and Tailwind CSS primitives.
- No `any` type escapes without documented rationale.

## 3. Error Handling & Logging
- Never catch and swallow exceptions blindly (`except: pass` is forbidden).
- Secrets and PII (Personal Identifiable Information) must never appear in log statements or stack traces.
- All errors returned by MCP tools must follow standard JSON-RPC error format with clear error codes.
