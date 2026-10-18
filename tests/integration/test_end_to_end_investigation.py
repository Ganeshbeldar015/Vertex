"""End-to-end integration test verifying complete GraphSleuth pipeline."""
from fastapi.testclient import TestClient

from src.data.generator import generate_synthetic_network
from src.graph.engine import PropertyGraph
from src.actions.service import ActionService
from src.mcp.server import SengraMCPServer
from src.agent.loop import InvestigationAgent
from src.agent.verifier import verify_citations
from src.api.server import create_app


def test_full_pipeline_alert_to_investigation_and_approval():
    """Validates end-to-end multi-hop slice from alert ingestion to UI API and approved freeze."""
    # 1. Initialize data & graph engine
    data = generate_synthetic_network(seed=42)
    engine = PropertyGraph()
    engine.load_dataset(data)

    # 2. Initialize action service & MCP server
    action_service = ActionService()
    mcp_server = SengraMCPServer(graph=engine, action_service=action_service)
    agent = InvestigationAgent(tool_client=mcp_server)

    # 3. Create FastAPI app
    app = create_app(engine=engine, action_service=action_service, agent=agent)
    client = TestClient(app)

    # 4. Step 1: Ingest/Fetch alerts
    alerts_resp = client.get("/api/alerts")
    assert alerts_resp.status_code == 200
    alerts = alerts_resp.json()
    hero_alert = next(a for a in alerts if a["account_id"] == "A-1042")
    assert hero_alert["severity"] in ["CRITICAL", "HIGH"]

    # 5. Step 2: Trigger investigation on hero account
    inv_resp = client.post("/api/investigate", json={"account_id": "A-1042", "alert_id": hero_alert["id"]})
    assert inv_resp.status_code == 200
    case_data = inv_resp.json()
    assert case_data["verdict"] == "FRAUD_RING_DETECTED"
    assert case_data["risk_score"] >= 0.75

    # 6. Step 3: Verify Cytoscape evidence subgraph
    elements = case_data["cytoscape_elements"]
    node_ids = {n["data"]["id"] for n in elements["nodes"]}
    assert "A-1042" in node_ids
    assert "A-1050" in node_ids
    assert "D-77" in node_ids

    # 7. Step 4: Verify citation faithfulness
    rationale = case_data["rationale"]
    evidence_nodes = [{"id": nid} for nid in node_ids]
    citation_res = verify_citations(rationale, {"nodes": evidence_nodes})
    assert citation_res["valid"] is True
    assert len(citation_res["unsupported_ids"]) == 0

    # 8. Step 5: Verify action approval workflow
    actions_resp = client.get("/api/actions")
    assert actions_resp.status_code == 200
    actions = actions_resp.json()
    pending_freeze = next(
        a for a in actions if a["status"] == "PENDING_APPROVAL" and a["type"] == "FREEZE_ACCOUNT"
    )
    action_id = pending_freeze["id"]

    # Approve freeze
    approve_resp = client.post(
        f"/api/actions/{action_id}/approve",
        json={"approver": "chief_risk_officer"}
    )
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "COMPLETED"

    # Verify state in ActionService
    assert action_service.is_account_frozen(pending_freeze["target"]) is True

    # 9. Step 6: Export case report
    case_id = case_data["case_id"]
    export_resp = client.get(f"/api/cases/{case_id}/export")
    assert export_resp.status_code == 200
    report_md = export_resp.text
    assert f"# Fraud Investigation Case Report: {case_id}" in report_md
    assert "A-1042" in report_md
    assert "FRAUD_RING_DETECTED" in report_md
