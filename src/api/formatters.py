"""Cytoscape graph element formatters and case report markdown generators."""
from typing import Any


def format_cytoscape_elements(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    ring_node_ids: set[str] | None = None,
    ring_edge_pairs: set[tuple[str, str]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Formats raw graph nodes and edges into Cytoscape.js elements."""
    ring_node_ids = ring_node_ids or set()
    ring_edge_pairs = ring_edge_pairs or set()

    formatted_nodes = []
    seen_nodes = set()
    for n in nodes:
        nid = n.get("id")
        if not nid or nid in seen_nodes:
            continue
        seen_nodes.add(nid)

        labels = n.get("labels", [])
        primary_label = labels[0] if labels else "Entity"
        props = n.get("properties", {})

        is_ring = (
            nid in ring_node_ids
            or props.get("flagged", False)
            or props.get("risk_score", 0.0) >= 0.7
        )

        formatted_nodes.append({
            "data": {
                "id": nid,
                "label": f"{primary_label} {nid}",
                "type": primary_label,
                "risk_score": props.get("risk_score", 0.0),
                "flagged": props.get("flagged", False),
                "is_ring": is_ring,
                "properties": props,
            }
        })

    formatted_edges = []
    seen_edges = set()
    for idx, e in enumerate(edges):
        src = e.get("source")
        tgt = e.get("target")
        etype = e.get("type", "CONNECTED_TO")
        eid = e.get("id", f"e_{src}_{tgt}_{etype}_{idx}")
        if not src or not tgt or eid in seen_edges:
            continue
        seen_edges.add(eid)

        props = e.get("properties", {})
        pair = (src, tgt)
        rev_pair = (tgt, src)
        is_ring = pair in ring_edge_pairs or rev_pair in ring_edge_pairs or (
            src in ring_node_ids and tgt in ring_node_ids
        )

        formatted_edges.append({
            "data": {
                "id": eid,
                "source": src,
                "target": tgt,
                "label": etype,
                "amount": props.get("amount", 0.0),
                "is_ring": is_ring,
                "properties": props,
            }
        })

    return {
        "nodes": formatted_nodes,
        "edges": formatted_edges,
    }


def format_case_report_markdown(case: dict[str, Any]) -> str:
    """Generates an auditor-ready Markdown case report from an investigation case object."""
    case_id = case.get("case_id", "CASE-UNKNOWN")
    account_id = case.get("account_id", "UNKNOWN")
    verdict = case.get("verdict", "INCONCLUSIVE")
    risk_score = case.get("risk_score", 0.0)
    risk_tier = case.get("risk_tier", "LOW")
    rationale = case.get("rationale", "")
    timeline = case.get("timeline", [])
    actions = case.get("recommended_actions", [])
    hypotheses = case.get("hypotheses_tested", [])

    lines = [
        f"# Fraud Investigation Case Report: {case_id}",
        "",
        "## Executive Summary",
        f"- **Target Account:** `{account_id}`",
        f"- **Investigation Verdict:** **{verdict}**",
        f"- **Risk Score:** {risk_score:.2f} ({risk_tier})",
        "",
        "## Agent Narrative & Rationale",
        rationale,
        "",
        "## Hypotheses Evaluated",
    ]

    for h in hypotheses:
        status = h.get("status", "UNTESTED")
        name = h.get("name", "Hypothesis")
        evidence = ", ".join(h.get("evidence", []))
        lines.append(f"- **{name}:** `{status}` (Evidence: {evidence})")

    lines.extend([
        "",
        "## Remediation Actions",
    ])
    if not actions:
        lines.append("_No actions queued or executed._")
    else:
        for a in actions:
            action_type = a.get("type")
            target = a.get("target")
            status = a.get("status")
            lines.append(f"- **{action_type}** on `{target}` -> Status: `{status}`")

    lines.extend([
        "",
        "## Investigation Tool Timeline",
    ])
    for step in timeline:
        tool = step.get("tool", "unknown")
        args = step.get("arguments", {})
        lines.append(f"- `Step`: Called `{tool}` with `{args}`")

    return "\n".join(lines) + "\n"
