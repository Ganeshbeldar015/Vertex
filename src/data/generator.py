"""Synthetic fraud network data generator."""
import random
from typing import Any


def generate_synthetic_network(seed: int = 42) -> dict[str, list[dict[str, Any]]]:
    """Generates a synthetic fraud network with seeded fraud rings and background nodes."""
    rng = random.Random(seed)
    nodes = []
    edges = []

    # 1. Hero Ring Nodes
    nodes.append({
        "id": "A-1042",
        "labels": ["Account"],
        "properties": {
            "type": "checking",
            "balance": 4500.0,
            "flagged": True,
            "risk_score": 0.85,
            "opened_at": "2026-01-10"
        }
    })
    nodes.append({
        "id": "A-1050",
        "labels": ["Account"],
        "properties": {
            "type": "savings",
            "balance": 12800.0,
            "flagged": False,
            "risk_score": 0.72,
            "opened_at": "2026-02-14"
        }
    })
    nodes.append({
        "id": "A-1061",
        "labels": ["Account"],
        "properties": {
            "type": "mule",
            "balance": 210.0,
            "flagged": False,
            "risk_score": 0.91,
            "opened_at": "2026-03-01"
        }
    })
    nodes.append({
        "id": "D-77",
        "labels": ["Device"],
        "properties": {
            "fingerprint": "fp_88b19a",
            "os": "Android 14"
        }
    })
    nodes.append({
        "id": "ALT-101",
        "labels": ["Alert"],
        "properties": {
            "account_id": "A-1042",
            "rule": "VELOCITY_AND_SHARED_DEVICE",
            "severity": "HIGH",
            "created_at": "2026-10-18T10:30:00Z"
        }
    })

    # 2. Hero Ring Relationships
    # Account -> Device links (Shared device)
    edges.append({
        "source": "A-1042",
        "target": "D-77",
        "type": "USED_DEVICE",
        "properties": {"first_used": "2026-02-01"}
    })
    edges.append({
        "source": "A-1050",
        "target": "D-77",
        "type": "USED_DEVICE",
        "properties": {"first_used": "2026-02-15"}
    })
    # Account -> Account transfers
    edges.append({
        "source": "A-1042",
        "target": "A-1050",
        "type": "TRANSFERRED_TO",
        "properties": {"amount": 3000.0, "ts": "2026-10-17T14:00:00Z"}
    })
    edges.append({
        "source": "A-1050",
        "target": "A-1061",
        "type": "TRANSFERRED_TO",
        "properties": {"amount": 2900.0, "ts": "2026-10-17T15:30:00Z"}
    })
    edges.append({
        "source": "A-1061",
        "target": "A-1042",
        "type": "TRANSFERRED_TO",
        "properties": {"amount": 2800.0, "ts": "2026-10-18T08:00:00Z"}
    })
    # Alert link
    edges.append({
        "source": "ALT-101",
        "target": "A-1042",
        "type": "TRIGGERED_ON",
        "properties": {}
    })

    # 3. Background legitimate nodes and edges
    for i in range(1, 15):
        acc_id = f"A-LEGIT-{i:03d}"
        dev_id = f"D-LEGIT-{i:03d}"
        nodes.append({
            "id": acc_id,
            "labels": ["Account"],
            "properties": {
                "type": "checking",
                "balance": float(rng.randint(500, 25000)),
                "flagged": False,
                "risk_score": round(rng.uniform(0.01, 0.25), 2),
                "opened_at": "2025-05-20"
            }
        })
        nodes.append({
            "id": dev_id,
            "labels": ["Device"],
            "properties": {
                "fingerprint": f"fp_legit_{i:03d}",
                "os": "iOS 17"
            }
        })
        edges.append({
            "source": acc_id,
            "target": dev_id,
            "type": "USED_DEVICE",
            "properties": {"first_used": "2025-06-01"}
        })

    return {"nodes": nodes, "edges": edges}
