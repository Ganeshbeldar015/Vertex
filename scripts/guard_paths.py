#!/usr/bin/env python3
"""Path and lane guard. Exits non-zero if changed files violate role allow-lists or locks."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def get_role_allowlist(role: str, root: Path = ROOT) -> list[str]:
    role_file = root / "harness" / "roles" / f"{role}.md"
    if not role_file.exists():
        return []
    text = role_file.read_text(encoding="utf-8")
    m = re.search(r"^#+\s*Allowed paths.*?\n(.*?)(?=^#+\s|\Z)", text, re.M | re.S | re.I)
    if not m:
        return []
    lines = [line.strip().lstrip("-* ").strip("`") for line in m.group(1).splitlines() if line.strip()]
    return [l for l in lines if l and not l.startswith("#")]


def path_matches_pattern(path: str, pattern: str) -> bool:
    clean_p = pattern.replace("\\", "/").rstrip("/")
    clean_path = path.replace("\\", "/")
    if clean_p.endswith("/**"):
        prefix = clean_p[:-3]
        return clean_path.startswith(prefix)
    if clean_p.endswith("/*"):
        prefix = clean_p[:-2]
        return clean_path.startswith(prefix) and "/" not in clean_path[len(prefix) + 1:]
    if "*" in clean_p:
        regex = re.escape(clean_p).replace(r"\*", ".*")
        return bool(re.match(f"^{regex}$", clean_path))
    return clean_path == clean_p or clean_path.startswith(clean_p + "/")


def check_paths(role: str, files: list[str], root: Path = ROOT) -> list[str]:
    allow_patterns = get_role_allowlist(role, root)
    if not allow_patterns:
        # Default allow-list from prompt.md if role file not yet created
        defaults = {
            "orchestrator": ["harness/state/**", "harness/logs/**", "AGENTS.md", "harness/profile.yaml", "docs/harness.md", "docs/raw.md", "CLAUDE.md", ".cursor/**", ".github/**", ".mcp.json", "scripts/**", "tests/**", "harness/**"],
            "po-spec": ["harness/artifacts/**/01-spec.md", "harness/tasks/**"],
            "designer": ["harness/artifacts/**/02-design.md", "docs/adr/**"],
            "tech-lead": ["harness/artifacts/**/03-plan.md", "docs/adr/**"],
            "test-author": ["tests/**", "harness/artifacts/**/04-tests.md"],
            "builder": ["src/**", "harness/artifacts/**/05-build*.md"],
            "reviewer": ["harness/artifacts/**/06-review.md"],
            "security": ["harness/artifacts/**/06b-security.md"],
            "qa": ["harness/artifacts/**/07-qa.md"],
            "scribe": ["docs/**", "harness/artifacts/**/08-docs.md", "README.md", "CHANGELOG.md"],
            "librarian": ["docs/memory/**", "AGENTS.md"]
        }
        allow_patterns = defaults.get(role, [])

    violations = []
    for f in files:
        norm_f = f.replace("\\", "/").lstrip("./")
        if not any(path_matches_pattern(norm_f, pat) for pat in allow_patterns):
            violations.append(norm_f)
    return violations


def main():
    parser = argparse.ArgumentParser(description="Guard file paths written by roles.")
    parser.add_argument("--role", required=True, help="Agent role name")
    parser.add_argument("--files", nargs="*", help="List of modified files (default: git diff --name-only)")
    args = parser.parse_args()

    files = args.files
    if files is None:
        try:
            res = subprocess.run(["git", "diff", "--name-only", "HEAD"], capture_output=True, text=True, check=True)
            files = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        except Exception:
            files = []

    violations = check_paths(args.role, files)
    if violations:
        print(f"GUARD REJECTED: Role '{args.role}' touched disallowed paths:")
        for v in violations:
            print(f"  - {v}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
