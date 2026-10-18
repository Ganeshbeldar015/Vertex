import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import guard_paths as gp  # noqa: E402


def test_guard_allows_valid_paths():
    assert gp.check_paths("builder", ["src/agent.py", "harness/artifacts/T-0001/05-build-main.md"]) == []
    assert gp.check_paths("test-author", ["tests/unit/test_graph.py", "harness/artifacts/T-0001/04-tests.md"]) == []
    assert gp.check_paths("po-spec", ["harness/artifacts/T-0001/01-spec.md", "harness/tasks/T-0001.md"]) == []


def test_guard_rejects_disallowed_paths():
    # Builder should not be writing directly to test files or AGENTS.md
    violations = gp.check_paths("builder", ["tests/unit/test_graph.py", "AGENTS.md"])
    assert "tests/unit/test_graph.py" in violations
    assert "AGENTS.md" in violations

    # PO-Spec should not touch source code
    violations_po = gp.check_paths("po-spec", ["src/main.py"])
    assert "src/main.py" in violations_po
