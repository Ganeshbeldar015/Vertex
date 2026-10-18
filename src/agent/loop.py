"""Autonomous multi-hop investigation agent loop."""
from typing import Any
from src.agent.verifier import verify_citations


class InvestigationAgent:
    """Orchestrates multi-hop graph investigation over MCP tools within step budgets."""

    def __init__(self, tool_client: Any, max_tool_calls: int = 15):
        self.tool_client = tool_client
        self.max_tool_calls = max_tool_calls

    def investigate_alert(self, alert_id: str, target_account_id: str) -> dict[str, Any]:
        """Conducts an end-to-end investigation on a triggered alert."""
        tool_calls: list[dict[str, Any]] = []
        working_subgraph: dict[str, list[dict[str, Any]]] = {"nodes": [], "edges": []}
        discovered_entities: set[str] = {target_account_id}

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

        # Step 3: Pattern Analysis
        # Check for shared devices and linked accounts
        devices = [n["id"] for n in dedup_nodes if "Device" in n.get("labels", [])]
        accounts = [n["id"] for n in dedup_nodes if "Account" in n.get("labels", [])]

        has_shared_device = len(devices) > 0 and len(accounts) >= 2
        has_transfers = any(e.get("type") == "TRANSFERRED_TO" for e in working_subgraph["edges"])

        # Step 4: Formulate Verdict
        if has_shared_device and has_transfers:
            verdict = "fraud_ring_detected"
            confidence = 0.88
            shared_dev = devices[0]
            linked_accs = [a for a in accounts if a != target_account_id]
            linked_acc_str = ", ".join(linked_accs)
            rationale = (
                f"Account {target_account_id} shares device {shared_dev} with {linked_acc_str}. "
                f"Transfers link {linked_acc_str} into a coordinated mule flow."
            )
        else:
            verdict = "inconclusive"
            confidence = 0.35
            rationale = f"Account {target_account_id} does not show strong multi-hop fraud ring indicators."

        # Step 5: Citation Verification
        citation_check = verify_citations(rationale, working_subgraph)

        return {
            "alert_id": alert_id,
            "target_account": target_account_id,
            "status": "completed",
            "verdict": verdict,
            "confidence": confidence,
            "discovered_entities": sorted(list(discovered_entities)),
            "tool_calls": tool_calls,
            "evidence_subgraph": working_subgraph,
            "rationale": rationale,
            "citations_verified": citation_check["valid"]
        }
