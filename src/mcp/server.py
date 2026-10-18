"""SENGRA Model Context Protocol (MCP) server implementation."""
from typing import Any
from src.graph.engine import PropertyGraph


class SengraMCPServer:
    """Dispatches graph investigation tools following MCP JSON-RPC patterns."""

    def __init__(self, graph: PropertyGraph):
        self.graph = graph

    def list_tools(self) -> list[dict[str, Any]]:
        """Returns the discoverable tool catalog with JSON schemas."""
        return [
            {
                "name": "graph.get_entity",
                "description": "Fetch a graph node and its properties by unique ID.",
                "inputSchema": {
                    "type": "object",
                    "required": ["entity_id"],
                    "properties": {
                        "entity_id": {"type": "string", "description": "Unique identifier of the entity"}
                    }
                },
                "category": "read",
                "cost": "cheap"
            },
            {
                "name": "graph.expand_neighborhood",
                "description": "Expand relationships up to N hops around an entity to find connected devices and accounts.",
                "inputSchema": {
                    "type": "object",
                    "required": ["entity_id"],
                    "properties": {
                        "entity_id": {"type": "string", "description": "Center entity identifier"},
                        "hops": {"type": "integer", "default": 2, "maximum": 4},
                        "limit": {"type": "integer", "default": 50}
                    }
                },
                "category": "read",
                "cost": "medium"
            }
        ]

    def handle_call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Executes a tool call and returns a structured response."""
        arguments = arguments or {}

        if tool_name == "graph.get_entity":
            entity_id = arguments.get("entity_id")
            if not entity_id:
                return {"status": "error", "error": "Missing required argument 'entity_id'"}
            node = self.graph.get_node(entity_id)
            return {"status": "ok", "result": node}

        elif tool_name == "graph.expand_neighborhood":
            entity_id = arguments.get("entity_id")
            if not entity_id:
                return {"status": "error", "error": "Missing required argument 'entity_id'"}
            hops = int(arguments.get("hops", 2))
            limit = int(arguments.get("limit", 50))
            subgraph = self.graph.expand_neighborhood(entity_id, hops=hops, limit=limit)
            return {"status": "ok", "result": subgraph}

        return {"status": "error", "error": f"Unknown tool '{tool_name}'"}
