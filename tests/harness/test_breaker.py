import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import breaker as br  # noqa: E402


def test_failure_signature_deterministic():
    sig1 = br.compute_failure_signature(["test_a", "test_b"], "AssertionError: expected 1 got 2")
    sig2 = br.compute_failure_signature(["test_b", "test_a"], "AssertionError: expected 1 got 2")
    assert sig1 == sig2
    assert len(sig1) == 16


def test_breaker_trips_on_critical_violations(tmp_path):
    (tmp_path / "harness" / "state").mkdir(parents=True)
    (tmp_path / "harness" / "logs").mkdir(parents=True)
    (tmp_path / "harness" / "state" / "budgets.json").write_text("{}", encoding="utf-8")
    (tmp_path / "harness" / "state" / "state.json").write_text('{"breaker": {"tripped": false}}', encoding="utf-8")

    tripped = br.check_and_trip("guard_violation", "builder modified tests/x.py", root=tmp_path)
    assert tripped is True

    state = br.load_json(tmp_path / "harness" / "state" / "state.json")
    assert state["breaker"]["tripped"] is True
    assert "guard_violation" in state["breaker"]["reason"]
