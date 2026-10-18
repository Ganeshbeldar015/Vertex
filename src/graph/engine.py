"""In-memory property graph engine with parameterized OpenCypher parsing and neighborhood expansion."""
import re
from typing import Any


class PropertyGraph:
    """In-memory property graph supporting node/edge storage and parameterized queries."""

    FORBIDDEN_WRITE_KEYWORDS = re.compile(
        r"\b(CREATE|MERGE|DETACH DELETE|DELETE|SET|DROP|ALTER)\b", re.IGNORECASE
    )

    def __init__(self):
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []
        self.adj_out: dict[str, list[dict[str, Any]]] = {}
        self.adj_in: dict[str, list[dict[str, Any]]] = {}

    def add_node(self, node_id: str, labels: list[str], properties: dict[str, Any] | None = None):
        """Adds or updates a node in the graph."""
        self.nodes[node_id] = {
            "id": node_id,
            "labels": labels or [],
            "properties": properties or {}
        }
        if node_id not in self.adj_out:
            self.adj_out[node_id] = []
        if node_id not in self.adj_in:
            self.adj_in[node_id] = []

    def add_edge(
        self,
        source: str,
        target: str,
        edge_type: str,
        properties: dict[str, Any] | None = None
    ):
        """Adds a directed relationship between two nodes."""
        edge = {
            "source": source,
            "target": target,
            "type": edge_type,
            "properties": properties or {}
        }
        self.edges.append(edge)
        self.adj_out.setdefault(source, []).append(edge)
        self.adj_in.setdefault(target, []).append(edge)

    def load_dataset(self, data: dict[str, list[dict[str, Any]]]):
        """Bulk loads nodes and edges from a generator dictionary."""
        for n in data.get("nodes", []):
            self.add_node(n["id"], n.get("labels", []), n.get("properties", {}))
        for e in data.get("edges", []):
            self.add_edge(e["source"], e["target"], e.get("type", "RELATED"), e.get("properties", {}))

    def get_node(self, node_id: str) -> dict[str, Any] | None:
        """Retrieves a single node by ID."""
        return self.nodes.get(node_id)

    def query(self, cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Executes a read-only Cypher query with strict parameter validation."""
        params = params or {}
        clean_cypher = cypher.strip()

        # Guard against write keywords in read-only queries
        if self.FORBIDDEN_WRITE_KEYWORDS.search(clean_cypher):
            raise ValueError("Write keywords forbidden in read-only query")

        # Basic Cypher pattern evaluator for MATCH (n:Label {id: $param})
        match_id_param = re.search(r"\{id:\s*\$([a-zA-Z0-9_]+)\}", clean_cypher)
        if match_id_param:
            param_key = match_id_param.group(1)
            target_id = params.get(param_key)
            if target_id and target_id in self.nodes:
                return [self.nodes[target_id]]
            return []

        # MATCH all nodes for label
        match_label = re.search(r"MATCH\s*\([a-zA-Z0-9_]*:([a-zA-Z0-9_]+)\)", clean_cypher)
        if match_label:
            target_label = match_label.group(1)
            return [n for n in self.nodes.values() if target_label in n["labels"]]

        return []

    def expand_neighborhood(
        self,
        entity_id: str,
        hops: int = 2,
        limit: int = 50
    ) -> dict[str, list[dict[str, Any]]]:
        """Expands N hops around an entity across incoming and outgoing edges."""
        if entity_id not in self.nodes:
            return {"nodes": [], "edges": []}

        visited_nodes: set[str] = {entity_id}
        frontier: set[str] = {entity_id}
        collected_edges: list[dict[str, Any]] = []

        for _ in range(hops):
            next_frontier: set[str] = set()
            for curr in frontier:
                # Outgoing edges
                for edge in self.adj_out.get(curr, []):
                    collected_edges.append(edge)
                    tgt = edge["target"]
                    if tgt not in visited_nodes:
                        visited_nodes.add(tgt)
                        next_frontier.add(tgt)
                # Incoming edges
                for edge in self.adj_in.get(curr, []):
                    collected_edges.append(edge)
                    src = edge["source"]
                    if src not in visited_nodes:
                        visited_nodes.add(src)
                        next_frontier.add(src)

            frontier = next_frontier
            if len(visited_nodes) >= limit:
                break

        # Deduplicate edges by (source, target, type)
        unique_edges = []
        seen_edges = set()
        for e in collected_edges:
            key = (e["source"], e["target"], e["type"])
            if key not in seen_edges:
                seen_edges.add(key)
                unique_edges.append(e)

        sub_nodes = [self.nodes[nid] for nid in visited_nodes if nid in self.nodes]
        return {
            "nodes": sub_nodes[:limit],
            "edges": unique_edges[:limit]
        }
