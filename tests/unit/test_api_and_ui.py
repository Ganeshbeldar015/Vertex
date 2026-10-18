"""Unit tests for FastAPI investigation endpoints, Cytoscape formatting, and explainability."""
import pytest
from fastapi.testclient import TestClient

from src.data.generator import generate_synthetic_network
from src.graph.engine import PropertyGraph
from src.actions.service import ActionService
from src.agent.loop import InvestigationAgent
from src.agent.verifier import verify_citations
from src.api.server import create_app


@pytest.fixture
def test_app():
    graph_data = generate_synthetic_network(seed=42)
    engine = PropertyGraph()
    engine.load_dataset(graph_data)
    from src.mcp.server import SengraMCPServer
    action_service = ActionService()
    mcp_server = SengraMCPServer(graph=engine, action_service=action_service)
    agent = InvestigationAgent(tool_client=mcp_server)
    app = create_app(engine=engine, action_service=action_service, agent=agent)
    return TestClient(app)


def test_root_and_health_endpoints(test_app):
    root_resp = test_app.get("/")
    assert root_resp.status_code == 200
    data = root_resp.json()
    assert data["status"] == "online"
    assert "endpoints" in data

    health_resp = test_app.get("/health")
    assert health_resp.status_code == 200
    assert health_resp.json()["status"] == "healthy"


def test_get_alerts_endpoint(test_app):
    response = test_app.get("/api/alerts")
    assert response.status_code == 200
    alerts = response.json()
    assert len(alerts) > 0
    # Must contain alert on hero account A-1042
    hero_alert = next((a for a in alerts if a["account_id"] == "A-1042"), None)
    assert hero_alert is not None
    assert hero_alert["severity"] in ["HIGH", "CRITICAL"]


def test_investigate_account_returns_cytoscape_and_timeline(test_app):
    response = test_app.post("/api/investigate", json={"account_id": "A-1042"})
    assert response.status_code == 200
    case_data = response.json()
    assert "case_id" in case_data
    assert case_data["verdict"] == "FRAUD_RING_DETECTED"
    assert case_data["risk_score"] >= 0.75
    assert len(case_data["timeline"]) > 0

    # Cytoscape elements verification
    elements = case_data["cytoscape_elements"]
    assert "nodes" in elements and "edges" in elements
    node_ids = [n["data"]["id"] for n in elements["nodes"]]
    assert "A-1042" in node_ids
    assert "A-1050" in node_ids
    assert "D-77" in node_ids

    # Check ring highlighting
    ring_nodes = [n for n in elements["nodes"] if n["data"].get("is_ring")]
    assert len(ring_nodes) >= 2


def test_case_export_markdown(test_app):
    inv_resp = test_app.post("/api/investigate", json={"account_id": "A-1042"})
    case_id = inv_resp.json()["case_id"]

    export_resp = test_app.get(f"/api/cases/{case_id}/export")
    assert export_resp.status_code == 200
    report = export_resp.text
    assert f"# Fraud Investigation Case Report: {case_id}" in report
    assert "A-1042" in report
    assert "Risk Score:" in report


def test_action_approval_api_workflow(test_app):
    # Trigger investigation so pending actions are queued
    test_app.post("/api/investigate", json={"account_id": "A-1042"})

    # Fetch actions
    actions_resp = test_app.get("/api/actions")
    assert actions_resp.status_code == 200
    actions = actions_resp.json()
    pending = [a for a in actions if a["status"] == "PENDING_APPROVAL"]
    assert len(pending) > 0

    action_to_approve = pending[0]
    action_id = action_to_approve["id"]

    # Approve action
    approve_resp = test_app.post(
        f"/api/actions/{action_id}/approve",
        json={"approver": "lead_analyst_sarah"}
    )
    assert approve_resp.status_code == 200
    approved_action = approve_resp.json()
    assert approved_action["status"] == "COMPLETED"
    assert approved_action["approver"] == "lead_analyst_sarah"

    # Reverse action
    reverse_resp = test_app.post(f"/api/actions/{action_id}/reverse")
    assert reverse_resp.status_code == 200
    reversed_action = reverse_resp.json()
    assert reversed_action["status"] == "REVERSED"


def test_citation_faithfulness_verification(test_app):
    inv_resp = test_app.post("/api/investigate", json={"account_id": "A-1042"})
    data = inv_resp.json()
    rationale = data["rationale"]
    evidence_nodes = [{"id": n["data"]["id"]} for n in data["cytoscape_elements"]["nodes"]]

    res = verify_citations(rationale, {"nodes": evidence_nodes})
    assert res["valid"] is True
    assert len(res["unsupported_ids"]) == 0
