"""Composite fraud risk scoring combining graph features and factor attributions."""
from typing import Any
from src.graph.algorithms import detect_cycles, find_shared_attributes, detect_communities


def compute_risk_score(graph: Any, account_id: str) -> dict[str, Any]:
    """Calculates a multi-factor risk score for an account using graph features."""
    if account_id not in graph.nodes:
        return {
            "account_id": account_id,
            "risk_score": 0.0,
            "tier": "LOW",
            "factors": []
        }

    # Factor 1: Shared Device Factor (Weight: 0.35)
    shared_devs = find_shared_attributes(graph, account_id, attribute_type="Device")
    shared_device_val = 0.0
    for s in shared_devs.get("shared_entities", []):
        if len(s.get("linked_entities", [])) >= 1:
            shared_device_val = 1.0
            break

    # Factor 2: Circular Flow Participation (Weight: 0.30)
    cycles_res = detect_cycles(graph, start_node=account_id, min_length=3, max_length=6)
    in_cycle = any(account_id in c.get("path", []) for c in cycles_res.get("cycles", []))
    circular_flow_val = 1.0 if in_cycle else 0.0

    # Factor 3: Community Density Factor (Weight: 0.20)
    comm_res = detect_communities(graph)
    comm_val = 0.0
    for c in comm_res.get("communities", []):
        if account_id in c.get("members", []):
            if c.get("size", 0) >= 3:
                comm_val = 0.75
            elif c.get("size", 0) >= 2:
                comm_val = 0.50
            break

    # Factor 4: High Velocity / Balance Ratio (Weight: 0.15)
    outgoing_count = len(graph.adj_out.get(account_id, []))
    velocity_val = min(1.0, outgoing_count * 0.4)

    # Weights
    w_device = 0.35
    w_cycle = 0.30
    w_comm = 0.20
    w_vel = 0.15

    total_score = round(
        (w_device * shared_device_val) +
        (w_cycle * circular_flow_val) +
        (w_comm * comm_val) +
        (w_vel * velocity_val),
        2
    )

    if total_score >= 0.70:
        tier = "HIGH"
    elif total_score >= 0.40:
        tier = "MEDIUM"
    else:
        tier = "LOW"

    factors = [
        {
            "name": "shared_device",
            "weight": w_device,
            "value": round(shared_device_val, 2),
            "contribution": round(w_device * shared_device_val, 3)
        },
        {
            "name": "circular_flow",
            "weight": w_cycle,
            "value": round(circular_flow_val, 2),
            "contribution": round(w_cycle * circular_flow_val, 3)
        },
        {
            "name": "community_density",
            "weight": w_comm,
            "value": round(comm_val, 2),
            "contribution": round(w_comm * comm_val, 3)
        },
        {
            "name": "high_velocity",
            "weight": w_vel,
            "value": round(velocity_val, 2),
            "contribution": round(w_vel * velocity_val, 3)
        }
    ]

    return {
        "account_id": account_id,
        "risk_score": total_score,
        "tier": tier,
        "factors": factors
    }
