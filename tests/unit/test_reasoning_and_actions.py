"""Unit tests for Sprint 3 Multi-Hop Reasoning & Action Layer (T-0003)."""
import pytest
from src.data.generator import generate_synthetic_network
from src.graph.engine import PropertyGraph
from src.graph.risk import compute_risk_score
from src.actions.service import ActionService
from src.mcp.server import SengraMCPServer
from src.agent.loop import InvestigationAgent


@pytest.fixture
def fraud_setup():
    """Sets up a complete environment with graph, action service, and MCP server."""
    data = generate_synthetic_network(seed=42)
    graph = PropertyGraph()
    graph.load_dataset(data)
    action_service = ActionService()
    server = SengraMCPServer(graph, action_service=action_service)
    return graph, action_service, server


def test_score_risk_computes_factor_breakdown(fraud_setup):
    """AC-003-a: score_risk computes composite score and factor breakdown."""
    graph, _, _ = fraud_setup
    result = compute_risk_score(graph, "A-1042")

    assert result["account_id"] == "A-1042"
    assert result["risk_score"] >= 0.75
    assert result["tier"] == "HIGH"
    assert "factors" in result

    factor_names = {f["name"] for f in result["factors"]}
    assert "shared_device" in factor_names
    assert "circular_flow" in factor_names
    assert "community_density" in factor_names


def test_agent_hypothesis_loop_investigates_ring(fraud_setup):
    """AC-003-b: Agent evaluates multi-hop hypotheses, scores risk, and recommends actions."""
    graph, action_service, server = fraud_setup
    agent = InvestigationAgent(tool_client=server)

    investigation = agent.investigate_alert("ALT-101", target_account_id="A-1042")

    assert investigation["status"] == "completed"
    assert investigation["verdict"] == "fraud_ring_detected"
    assert investigation["confidence"] >= 0.75
    assert len(investigation["tool_calls"]) <= 15
    assert "hypotheses_tested" in investigation
    assert "shared_device_collusion" in investigation["hypotheses_tested"]

    # Verify action recommendations
    assert "recommended_actions" in investigation
    rec_types = [a["type"] for a in investigation["recommended_actions"]]
    assert "FREEZE_ACCOUNT" in rec_types
    assert "BLOCK_DEVICE" in rec_types


def test_action_service_queues_gated_freeze(fraud_setup):
    """AC-003-c: High-risk freeze and block actions enter PENDING_APPROVAL status."""
    _, action_service, _ = fraud_setup
    case_id = action_service.create_case("Fraud Ring Investigation", ["A-1042", "A-1050"], "Suspected mule loop")

    # Flag entity executes automatically
    flag_rec = action_service.flag_entity(case_id, "A-1042", "Shared device with mule", ["E1"])
    assert flag_rec["status"] == "AUTO_EXECUTED"

    # Freeze account enters PENDING_APPROVAL
    freeze_rec = action_service.freeze_account(case_id, "A-1042", "Suspected mule coordinator", ["E1", "E2"])
    assert freeze_rec["status"] == "PENDING_APPROVAL"
    assert freeze_rec["approver"] is None

    # Block device enters PENDING_APPROVAL
    block_rec = action_service.block_device(case_id, "D-77", "Device tied to multiple accounts", ["E1"])
    assert block_rec["status"] == "PENDING_APPROVAL"


def test_action_approval_and_reversibility(fraud_setup):
    """AC-003-d: Queued action can be approved and subsequently reversed."""
    _, action_service, _ = fraud_setup
    case_id = action_service.create_case("Case 1", ["A-1042"], "Summary")
    freeze_rec = action_service.freeze_account(case_id, "A-1042", "Reason", ["E1"])

    # Approve action
    appr_rec = action_service.approve_action(freeze_rec["action_id"], approver_id="OFFICER-42")
    assert appr_rec["status"] == "APPROVED"
    assert appr_rec["approver"] == "OFFICER-42"
    assert action_service.is_account_frozen("A-1042") is True

    # Reverse action (unfreeze)
    rev_rec = action_service.reverse_action(freeze_rec["action_id"], reason="Customer verified legitimate", approver_id="OFFICER-42")
    assert rev_rec["status"] == "REVERSED"
    assert action_service.is_account_frozen("A-1042") is False


def test_action_log_maintains_immutable_audit(fraud_setup):
    """AC-003-e: ActionLog records all actions with idempotency and audit metadata."""
    _, action_service, _ = fraud_setup
    case_id = action_service.create_case("Audit Case", ["A-1042"], "Audit Summary")

    # Idempotent call with key
    r1 = action_service.flag_entity(case_id, "A-1042", "Reason", ["E1"], idempotency_key="KEY-999")
    r2 = action_service.flag_entity(case_id, "A-1042", "Reason", ["E1"], idempotency_key="KEY-999")
    assert r1["action_id"] == r2["action_id"]

    # Verify audit log
    log = action_service.get_action_log(case_id=case_id)
    assert len(log) == 1
    entry = log[0]
    assert entry["case_id"] == case_id
    assert entry["target_id"] == "A-1042"
    assert "timestamp" in entry


def test_mcp_action_tool_dispatch(fraud_setup):
    """MCP Contract: Server dispatches action tools and returns structured results."""
    _, _, server = fraud_setup
    tools = {t["name"] for t in server.list_tools()}

    assert "algo.score_risk" in tools
    assert "action.create_case" in tools
    assert "action.flag_entity" in tools
    assert "action.freeze_account" in tools
    assert "action.approve_action" in tools

    # Test create_case via MCP
    case_resp = server.handle_call("action.create_case", {
        "title": "MCP Case",
        "entity_ids": ["A-1042"],
        "summary": "Created via MCP"
    })
    assert case_resp["status"] == "ok"
    case_id = case_resp["result"]["case_id"]

    # Test freeze_account via MCP
    freeze_resp = server.handle_call("action.freeze_account", {
        "case_id": case_id,
        "account_id": "A-1042",
        "reason": "Test freeze",
        "evidence_ids": ["E1"]
    })
    assert freeze_resp["status"] == "ok"
    assert freeze_resp["result"]["status"] == "PENDING_APPROVAL"
