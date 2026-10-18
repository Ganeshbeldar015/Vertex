"""Citation verifier asserting all claims reference real entities in tool outputs."""
import re
from typing import Any

ENTITY_ID_PATTERN = re.compile(r"\b(A-[0-9A-Za-z_-]+|D-[0-9A-Za-z_-]+|ALT-[0-9A-Za-z_-]+)\b")


def verify_citations(rationale: str, tool_outputs: dict[str, Any]) -> dict[str, Any]:
    """Validates that every cited entity ID in the rationale exists in the provided tool outputs."""
    cited_ids = set(ENTITY_ID_PATTERN.findall(rationale))

    # Extract all known IDs from tool outputs
    known_ids: set[str] = set()
    for node in tool_outputs.get("nodes", []):
        if "id" in node:
            known_ids.add(node["id"])

    for edge in tool_outputs.get("edges", []):
        if "source" in edge:
            known_ids.add(edge["source"])
        if "target" in edge:
            known_ids.add(edge["target"])

    unsupported_ids = sorted(list(cited_ids - known_ids))

    return {
        "valid": len(unsupported_ids) == 0,
        "cited_ids": sorted(list(cited_ids)),
        "unsupported_ids": unsupported_ids,
        "faithfulness_score": 1.0 if not cited_ids or not unsupported_ids else (
            (len(cited_ids) - len(unsupported_ids)) / len(cited_ids)
        )
    }
