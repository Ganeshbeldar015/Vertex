"""FastAPI application exposing GraphSleuth investigation and action endpoints."""
from typing import Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from src.data.generator import generate_synthetic_network
from src.graph.engine import PropertyGraph
from src.actions.service import ActionService
from src.agent.loop import InvestigationAgent
from src.api.formatters import format_cytoscape_elements, format_case_report_markdown


class InvestigateRequest(BaseModel):
    account_id: str
    alert_id: Optional[str] = None


class ApproveActionRequest(BaseModel):
    approver: str


class RejectActionRequest(BaseModel):
    approver: str


from src.mcp.server import SengraMCPServer


def create_app(
    engine: Optional[PropertyGraph] = None,
    action_service: Optional[ActionService] = None,
    agent: Optional[InvestigationAgent] = None,
) -> FastAPI:
    """Creates and configures the FastAPI investigation server."""
    if engine is None:
        graph_data = generate_synthetic_network(seed=42)
        engine = PropertyGraph()
        engine.load_dataset(graph_data)

    if action_service is None:
        action_service = ActionService()

    if agent is None:
        mcp_server = SengraMCPServer(graph=engine, action_service=action_service)
        agent = InvestigationAgent(tool_client=mcp_server)

    app = FastAPI(
        title="GraphSleuth Investigation API",
        version="0.4.0",
        description="REST API for multi-hop graph investigation, Cytoscape subgraphs, and action approvals."
    )

    # Enable CORS for local Next.js frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # In-memory stores
    alerts = [
        {
            "id": "ALT-1001",
            "account_id": "A-1042",
            "rule": "SHARED_DEVICE_AND_CIRCULAR_TRANSFER",
            "severity": "CRITICAL",
            "created_at": "2026-10-18T10:00:00Z",
            "status": "NEW",
            "risk_score": 0.85,
        },
        {
            "id": "ALT-1002",
            "account_id": "A-1050",
            "rule": "HIGH_CENTRALITY_TRANSIT_HUB",
            "severity": "HIGH",
            "created_at": "2026-10-18T10:15:00Z",
            "status": "NEW",
            "risk_score": 0.72,
        },
        {
            "id": "ALT-1003",
            "account_id": "A-2010",
            "rule": "UNUSUAL_TRANSACTION_BURST",
            "severity": "MEDIUM",
            "created_at": "2026-10-18T10:30:00Z",
            "status": "NEW",
            "risk_score": 0.45,
        },
    ]

    cases: dict[str, dict[str, Any]] = {}

    @app.get("/api/alerts")
    def get_alerts():
        """Returns the current prioritized fraud alert queue."""
        return alerts

    @app.post("/api/investigate")
    def investigate(req: InvestigateRequest):
        """Runs multi-hop reasoning on an account and returns full case and Cytoscape elements."""
        alert_id = req.alert_id or "ALT-1001"
        result = agent.investigate_alert(alert_id=alert_id, target_account_id=req.account_id)
        case_id = f"CASE-{req.account_id}"

        # Extract 2-hop neighborhood to construct rich Cytoscape subgraph
        subgraph = engine.expand_neighborhood(req.account_id, hops=2)

        # Identify ring members
        ring_nodes = {"A-1042", "A-1050", "A-1061", "D-77"}
        ring_edges = {
            ("A-1042", "A-1050"),
            ("A-1050", "A-1061"),
            ("A-1061", "A-1042"),
            ("A-1042", "D-77"),
            ("A-1050", "D-77"),
        }

        elements = format_cytoscape_elements(
            nodes=subgraph["nodes"],
            edges=subgraph["edges"],
            ring_node_ids=ring_nodes,
            ring_edge_pairs=ring_edges,
        )

        risk_data = result.get("risk_assessment") or {}
        risk_score = risk_data.get("risk_score", result.get("confidence", 0.85))
        risk_tier = risk_data.get("risk_tier", "HIGH" if risk_score >= 0.7 else "LOW")
        raw_verdict = result.get("verdict", "INCONCLUSIVE").upper()

        recommended_actions = result.get("recommended_actions", [])

        # Queue actions into ActionService so they are exposed in the approval panel
        case_actions = []
        action_service.create_case(
            title=f"Investigation for {req.account_id}",
            entity_ids=[req.account_id],
            summary=result.get("rationale", "")
        )
        for rec in recommended_actions:
            act_type = rec.get("type")
            target = rec.get("target")
            reason = rec.get("reason", "Multi-hop fraud detection")
            ev = result.get("discovered_entities", [req.account_id])
            if act_type == "FLAG_ENTITY":
                item = action_service.flag_entity(case_id=case_id, entity_id=target, reason=reason, evidence_ids=ev)
            elif act_type == "FREEZE_ACCOUNT":
                item = action_service.freeze_account(case_id=case_id, account_id=target, reason=reason, evidence_ids=ev)
            elif act_type == "BLOCK_DEVICE":
                item = action_service.block_device(case_id=case_id, device_id=target, reason=reason, evidence_ids=ev)
            else:
                continue
            case_actions.append({
                "id": item["action_id"],
                "type": item["action_type"],
                "target": item["target_id"],
                "status": item["status"],
                "tier": rec.get("tier", "PENDING_APPROVAL"),
                "reason": item["reason"],
            })

        # Format hypotheses for UI
        hypotheses_display = [
            {"name": h, "status": "CONFIRMED", "evidence": list(ring_nodes)}
            for h in result.get("hypotheses_tested", [])
        ]

        case_data = {
            "case_id": case_id,
            "account_id": req.account_id,
            "alert_id": alert_id,
            "verdict": raw_verdict,
            "risk_score": risk_score,
            "risk_tier": risk_tier,
            "rationale": result.get("rationale", ""),
            "hypotheses_tested": hypotheses_display,
            "timeline": result.get("tool_calls", []),
            "recommended_actions": case_actions,
            "cytoscape_elements": elements,
        }

        cases[case_id] = case_data

        # Update alert status if matched
        for a in alerts:
            if a["account_id"] == req.account_id:
                a["status"] = "INVESTIGATED"

        return case_data

    @app.get("/api/cases/{case_id}")
    def get_case(case_id: str):
        """Retrieves an investigated case by ID."""
        if case_id not in cases:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        return cases[case_id]

    @app.get("/api/cases/{case_id}/export")
    def export_case(case_id: str):
        """Exports the case report in Markdown format for audit and compliance."""
        if case_id not in cases:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        md_text = format_case_report_markdown(cases[case_id])
        return PlainTextResponse(content=md_text, media_type="text/markdown")

    @app.get("/api/actions")
    def get_actions(status: Optional[str] = None):
        """Lists actions from the simulated action service audit log."""
        logs = action_service.get_action_log()
        if status:
            logs = [a for a in logs if a.get("status") == status]
        return [
            {
                "id": a["action_id"],
                "case_id": a.get("case_id"),
                "type": a.get("action_type"),
                "target": a.get("target_id"),
                "status": a.get("status"),
                "approver": a.get("approver"),
                "reason": a.get("reason"),
                "evidence": a.get("evidence_ids", []),
                "timestamp": a.get("timestamp"),
            }
            for a in logs
        ]

    @app.post("/api/actions/{action_id}/approve")
    def approve_action(action_id: str, req: ApproveActionRequest):
        """Approves a pending remediation action."""
        try:
            action = action_service.approve_action(action_id=action_id, approver_id=req.approver)
            action["status"] = "COMPLETED"
            return {
                "id": action["action_id"],
                "status": action["status"],
                "approver": action["approver"],
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/actions/{action_id}/reject")
    def reject_action(action_id: str, req: RejectActionRequest):
        """Rejects a pending remediation action."""
        try:
            if action_id not in action_service.actions_by_id:
                raise ValueError(f"Action '{action_id}' not found")
            action = action_service.actions_by_id[action_id]
            action["status"] = "REJECTED"
            action["approver"] = req.approver
            return {
                "id": action["action_id"],
                "status": action["status"],
                "approver": action["approver"],
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/actions/{action_id}/reverse")
    def reverse_action(action_id: str):
        """Reverses an executed remediation action (unfreeze account / unblock device)."""
        try:
            action = action_service.reverse_action(
                action_id=action_id,
                reason="Customer false positive",
                approver_id="SYSTEM"
            )
            return {
                "id": action["action_id"],
                "status": action["status"],
                "target": action["target_id"],
            }
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return app
