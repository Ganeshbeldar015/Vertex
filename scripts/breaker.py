#!/usr/bin/env python3
"""Circuit breaker evaluator. Trips execution on safety or thrashing thresholds."""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def compute_failure_signature(test_names: list[str], error_text: str) -> str:
    raw = f"{sorted(test_names)}|{error_text.strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def load_json(p: Path) -> dict:
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_json(p: Path, data: dict):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")


def check_and_trip(
    condition: str,
    evidence: str,
    root: Path = ROOT,
    stage: str = "unknown",
    task_id: str = "T-0000"
) -> bool:
    """Checks if breaker should trip. Returns True if tripped."""
    budgets = load_json(root / "harness" / "state" / "budgets.json")
    state = load_json(root / "harness" / "state" / "state.json")

    tripped = False
    reason = ""

    # Direct trip conditions
    if condition in ("guard_violation", "forbidden_tool", "unapproved_tool"):
        tripped = True
        reason = f"Immediate breaker trip on critical policy violation: {condition}. Evidence: {evidence}"
    elif condition == "stage_retry_exceeded":
        tripped = True
        reason = f"Stage retry budget exceeded. Evidence: {evidence}"
    elif condition == "identical_failures":
        tripped = True
        reason = f"Identical failure loop detected repeatedly. Evidence: {evidence}"
    elif condition == "diff_limit_exceeded":
        tripped = True
        reason = f"Diff size exceeded budget limits (probable scope creep). Evidence: {evidence}"
    elif condition == "no_progress":
        tripped = True
        reason = f"No progress across consecutive iterations. Evidence: {evidence}"
    elif condition == "budget_exhaustion":
        tripped = True
        reason = f"Session time or tool call budget exhausted. Evidence: {evidence}"
    elif condition == "malformed_artifact":
        tripped = True
        reason = f"Malformed artifact or handoff contract. Evidence: {evidence}"

    if tripped:
        # Trip state
        if "breaker" not in state:
            state["breaker"] = {}
        state["breaker"]["tripped"] = True
        state["breaker"]["reason"] = reason
        state["updated_at"] = datetime.now().isoformat()
        save_json(root / "harness" / "state" / "state.json", state)

        # Log failure
        failures_log = root / "harness" / "logs" / "failures.log.md"
        failures_log.parent.mkdir(parents=True, exist_ok=True)
        log_entry = (
            f"\n### F-{datetime.now().strftime('%Y%m%d%H%M%S')} | {task_id} | {stage} | TRIP\n"
            f"- **Reason:** {reason}\n"
            f"- **Evidence:** {evidence}\n"
            f"- **Timestamp:** {datetime.now().isoformat()}\n"
        )
        with failures_log.open("a", encoding="utf-8") as f:
            f.write(log_entry)

    return tripped


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        state = load_json(ROOT / "harness" / "state" / "state.json")
        breaker = state.get("breaker", {})
        if breaker.get("tripped"):
            print(f"TRIPPED: {breaker.get('reason')}")
            return 1
        print("BREAKER OK")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
