"""Autonomous multi-hop investigation agent loop with hypothesis testing and action recommendations."""
from typing import Any
from src.agent.verifier import verify_citations


class InvestigationAgent:
    """Orchestrates multi-hop graph investigation over MCP tools within step budgets."""

    def __init__(self, tool_client: Any, max_tool_calls: int = 15):
        self.tool_client = tool_client
        self.max_tool_calls = max_tool_calls

    def investigate_alert(self, alert_id: str, target_account_id: str) -> dict[str, Any]:
        """Conducts an end-to-end multi-hop investigation testing explicit fraud hypotheses."""
        tool_calls: list[dict[str, Any]] = []
        working_subgraph: dict[str, list[dict[str, Any]]] = {"nodes": [], "edges": []}
        discovered_entities: set[str] = {target_account_id}
        hypotheses_tested: list[str] = []
        recommended_actions: list[dict[str, Any]] = []

        # Step 1: Fetch target entity
        if len(tool_calls) < self.max_tool_calls:
            call_record = {"tool": "graph.get_entity", "args": {"entity_id": target_account_id}}
            resp = self.tool_client.handle_call("graph.get_entity", {"entity_id": target_account_id})
            call_record["result"] = resp
            tool_calls.append(call_record)
            if resp.get("status") == "ok" and resp.get("result"):
                working_subgraph["nodes"].append(resp["result"])

        # Step 2: Expand neighborhood around target account (2 hops)
        if len(tool_calls) < self.max_tool_calls:
            call_record = {
                "tool": "graph.expand_neighborhood",
                "args": {"entity_id": target_account_id, "hops": 2}
            }
            resp = self.tool_client.handle_call(
                "graph.expand_neighborhood",
                {"entity_id": target_account_id, "hops": 2}
            )
            call_record["result"] = resp
            tool_calls.append(call_record)
            if resp.get("status") == "ok" and resp.get("result"):
                sub = resp["result"]
                working_subgraph["nodes"].extend(sub.get("nodes", []))
                working_subgraph["edges"].extend(sub.get("edges", []))
                for n in sub.get("nodes", []):
                    discovered_entities.add(n["id"])

        # Deduplicate working subgraph
        seen_node_ids = set()
        dedup_nodes = []
        for n in working_subgraph["nodes"]:
            if n["id"] not in seen_node_ids:
                seen_node_ids.add(n["id"])
                dedup_nodes.append(n)
        working_subgraph["nodes"] = dedup_nodes

        # Step 3: Test Hypothesis 1 — Shared Device Collusion
        hypotheses_tested.append("shared_device_collusion")
        shared_devices_found = []
        if len(tool_calls) < self.max_tool_calls:
            call_record = {
                "tool": "graph.shared_attributes",
                "args": {"entity_id": target_account_id, "attribute_type": "Device"}
            }
            resp = self.tool_client.handle_call(
                "graph.shared_attributes",
                {"entity_id": target_account_id, "attribute_type": "Device"}
            )
            call_record["result"] = resp
            tool_calls.append(call_record)
            if resp.get("status") == "ok":
                shared_devices_found = resp.get("result", {}).get("shared_entities", [])

        # Step 4: Test Hypothesis 2 — Circular Money Laundering Flow
        hypotheses_tested.append("circular_money_flow")
        cycles_found = []
        if len(tool_calls) < self.max_tool_calls:
            call_record = {
                "tool": "algo.detect_cycles",
                "args": {"start_node": target_account_id, "min_length": 3, "max_length": 6}
            }
            resp = self.tool_client.handle_call(
                "algo.detect_cycles",
                {"start_node": target_account_id, "min_length": 3, "max_length": 6}
            )
            call_record["result"] = resp
            tool_calls.append(call_record)
            if resp.get("status") == "ok":
                cycles_found = resp.get("result", {}).get("cycles", [])

        # Step 5: Score Risk via Composite Tool
        risk_data = {"risk_score": 0.5, "tier": "MEDIUM", "factors": []}
        if len(tool_calls) < self.max_tool_calls:
            call_record = {"tool": "algo.score_risk", "args": {"account_id": target_account_id}}
            resp = self.tool_client.handle_call("algo.score_risk", {"account_id": target_account_id})
            call_record["result"] = resp
            tool_calls.append(call_record)
            if resp.get("status") == "ok":
                risk_data = resp.get("result", {})

        # Extract key entities for reporting and action planning
        devices = [n["id"] for n in dedup_nodes if "Device" in n.get("labels", [])]
        accounts = [n["id"] for n in dedup_nodes if "Account" in n.get("labels", [])]
        linked_accounts = [a for a in accounts if a != target_account_id]

        is_fraud_ring = (
            (len(shared_devices_found) > 0 or len(cycles_found) > 0) and
            risk_data.get("risk_score", 0.0) >= 0.50
        )

        if is_fraud_ring:
            verdict = "fraud_ring_detected"
            confidence = risk_data.get("risk_score", 0.88)
            discovered_entities.update(accounts)
            discovered_entities.update(devices)

            parts = []
            if shared_devices_found:
                shared_dev_id = shared_devices_found[0]["attribute_id"]
                linked_str = ", ".join(linked_accounts)
                parts.append(f"Account {target_account_id} shares device {shared_dev_id} with {linked_str}.")
            if cycles_found:
                linked_str = ", ".join(linked_accounts)
                parts.append(f"Transfers complete a circular money flow among {linked_str} and {target_account_id}.")
            if not parts:
                parts.append(f"Account {target_account_id} exhibits anomalous fraud risk.")
            rationale = " ".join(parts)

            # Recommend actions per decision policy
            recommended_actions.append({
                "type": "FLAG_ENTITY",
                "target": target_account_id,
                "tier": "AUTO",
                "reason": "Suspected fraud ring coordinator"
            })
            for acc in linked_accounts:
                recommended_actions.append({
                    "type": "FREEZE_ACCOUNT",
                    "target": acc,
                    "tier": "PENDING_APPROVAL",
                    "reason": "Participant in fraud cluster"
                })
            recommended_actions.append({
                "type": "FREEZE_ACCOUNT",
                "target": target_account_id,
                "tier": "PENDING_APPROVAL",
                "reason": "Primary suspect in fraud ring alert"
            })
            if devices:
                recommended_actions.append({
                    "type": "BLOCK_DEVICE",
                    "target": devices[0],
                    "tier": "PENDING_APPROVAL",
                    "reason": f"Device associated with fraud cluster"
                })
        else:
            verdict = "inconclusive"
            confidence = risk_data.get("risk_score", 0.35)
            rationale = f"Account {target_account_id} does not show strong multi-hop fraud ring indicators."

        # Step 6: Verify Citations
        citation_check = verify_citations(rationale, working_subgraph)

        return {
            "alert_id": alert_id,
            "target_account": target_account_id,
            "status": "completed",
            "verdict": verdict,
            "confidence": confidence,
            "discovered_entities": sorted(list(discovered_entities)),
            "hypotheses_tested": hypotheses_tested,
            "recommended_actions": recommended_actions,
            "risk_assessment": risk_data,
            "tool_calls": tool_calls,
            "evidence_subgraph": working_subgraph,
            "rationale": rationale,
            "citations_verified": citation_check["valid"]
        }
