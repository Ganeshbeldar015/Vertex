"""SENGRA Model Context Protocol (MCP) server implementation with graph, algorithm, and action tools."""
from typing import Any
from src.graph.engine import PropertyGraph
from src.graph.algorithms import (
    detect_communities,
    rank_centrality,
    detect_cycles,
    find_paths,
    find_shared_attributes
)
from src.graph.risk import compute_risk_score
from src.actions.service import ActionService


class SengraMCPServer:
    """Dispatches graph investigation and action tools following MCP JSON-RPC patterns."""

    def __init__(self, graph: PropertyGraph, action_service: ActionService | None = None):
        self.graph = graph
        self.action_service = action_service or ActionService()

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
            },
            {
                "name": "algo.detect_communities",
                "description": "Detect communities and clusters of colluding accounts and shared devices.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subgraph_nodes": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "category": "algorithm",
                "cost": "expensive"
            },
            {
                "name": "algo.rank_centrality",
                "description": "Compute PageRank centrality to identify transaction hubs and money mules.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "subgraph_nodes": {"type": "array", "items": {"type": "string"}},
                        "damping_factor": {"type": "number", "default": 0.85},
                        "max_iterations": {"type": "integer", "default": 20},
                        "top_k": {"type": "integer", "default": 10}
                    }
                },
                "category": "algorithm",
                "cost": "expensive"
            },
            {
                "name": "algo.detect_cycles",
                "description": "Detect circular money flows and transfer loops where funds cycle back to origin.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "start_node": {"type": "string"},
                        "min_length": {"type": "integer", "default": 3},
                        "max_length": {"type": "integer", "default": 6}
                    }
                },
                "category": "algorithm",
                "cost": "expensive"
            },
            {
                "name": "graph.find_paths",
                "description": "Find the shortest relationship path between two entities.",
                "inputSchema": {
                    "type": "object",
                    "required": ["source_id", "target_id"],
                    "properties": {
                        "source_id": {"type": "string"},
                        "target_id": {"type": "string"},
                        "max_hops": {"type": "integer", "default": 4}
                    }
                },
                "category": "query",
                "cost": "medium"
            },
            {
                "name": "graph.shared_attributes",
                "description": "Find accounts sharing devices, IPs, addresses, or phone numbers.",
                "inputSchema": {
                    "type": "object",
                    "required": ["entity_id"],
                    "properties": {
                        "entity_id": {"type": "string"},
                        "attribute_type": {"type": "string", "default": "Device"}
                    }
                },
                "category": "query",
                "cost": "cheap"
            },
            {
                "name": "graph.run_readonly_cypher",
                "description": "Execute a guarded, read-only parameterized Cypher query with strict mutation guards.",
                "inputSchema": {
                    "type": "object",
                    "required": ["query"],
                    "properties": {
                        "query": {"type": "string"},
                        "params": {"type": "object", "default": {}}
                    }
                },
                "category": "query",
                "cost": "medium"
            },
            {
                "name": "algo.score_risk",
                "description": "Calculate composite fraud risk score and feature contribution breakdown for an account.",
                "inputSchema": {
                    "type": "object",
                    "required": ["account_id"],
                    "properties": {
                        "account_id": {"type": "string"}
                    }
                },
                "category": "analytic",
                "cost": "medium"
            },
            {
                "name": "action.create_case",
                "description": "Open an investigation case linking entities.",
                "inputSchema": {
                    "type": "object",
                    "required": ["title", "entity_ids", "summary"],
                    "properties": {
                        "title": {"type": "string"},
                        "entity_ids": {"type": "array", "items": {"type": "string"}},
                        "summary": {"type": "string"}
                    }
                },
                "category": "action",
                "cost": "cheap"
            },
            {
                "name": "action.flag_entity",
                "description": "Flag an entity as suspicious (Auto-executed).",
                "inputSchema": {
                    "type": "object",
                    "required": ["case_id", "entity_id", "reason"],
                    "properties": {
                        "case_id": {"type": "string"},
                        "entity_id": {"type": "string"},
                        "reason": {"type": "string"},
                        "evidence_ids": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "category": "action",
                "cost": "cheap"
            },
            {
                "name": "action.freeze_account",
                "description": "Queue an account freeze for review/approval.",
                "inputSchema": {
                    "type": "object",
                    "required": ["case_id", "account_id", "reason"],
                    "properties": {
                        "case_id": {"type": "string"},
                        "account_id": {"type": "string"},
                        "reason": {"type": "string"},
                        "evidence_ids": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "category": "action",
                "cost": "gated"
            },
            {
                "name": "action.block_device",
                "description": "Queue a device block for review/approval.",
                "inputSchema": {
                    "type": "object",
                    "required": ["case_id", "device_id", "reason"],
                    "properties": {
                        "case_id": {"type": "string"},
                        "device_id": {"type": "string"},
                        "reason": {"type": "string"},
                        "evidence_ids": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "category": "action",
                "cost": "gated"
            },
            {
                "name": "action.approve_action",
                "description": "Approve and execute a gated action.",
                "inputSchema": {
                    "type": "object",
                    "required": ["action_id", "approver_id"],
                    "properties": {
                        "action_id": {"type": "string"},
                        "approver_id": {"type": "string"}
                    }
                },
                "category": "action",
                "cost": "confirm"
            }
        ]

    def handle_call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Executes a tool call and returns a structured response."""
        arguments = arguments or {}

        try:
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

            elif tool_name == "algo.detect_communities":
                subgraph_nodes = arguments.get("subgraph_nodes")
                result = detect_communities(self.graph, subgraph_nodes=subgraph_nodes)
                return {"status": "ok", "result": result}

            elif tool_name == "algo.rank_centrality":
                subgraph_nodes = arguments.get("subgraph_nodes")
                damping_factor = float(arguments.get("damping_factor", 0.85))
                max_iter = int(arguments.get("max_iterations", 20))
                top_k = int(arguments.get("top_k", 10))
                result = rank_centrality(
                    self.graph,
                    subgraph_nodes=subgraph_nodes,
                    damping_factor=damping_factor,
                    max_iter=max_iter,
                    top_k=top_k
                )
                return {"status": "ok", "result": result}

            elif tool_name == "algo.detect_cycles":
                start_node = arguments.get("start_node")
                min_len = int(arguments.get("min_length", 3))
                max_len = int(arguments.get("max_length", 6))
                result = detect_cycles(self.graph, start_node=start_node, min_length=min_len, max_length=max_len)
                return {"status": "ok", "result": result}

            elif tool_name == "graph.find_paths":
                source_id = arguments.get("source_id")
                target_id = arguments.get("target_id")
                if not source_id or not target_id:
                    return {"status": "error", "error": "Missing required arguments 'source_id' and 'target_id'"}
                max_hops = int(arguments.get("max_hops", 4))
                result = find_paths(self.graph, source_id, target_id, max_hops=max_hops)
                return {"status": "ok", "result": result}

            elif tool_name == "graph.shared_attributes":
                entity_id = arguments.get("entity_id")
                if not entity_id:
                    return {"status": "error", "error": "Missing required argument 'entity_id'"}
                attr_type = arguments.get("attribute_type", "Device")
                result = find_shared_attributes(self.graph, entity_id, attribute_type=attr_type)
                return {"status": "ok", "result": result}

            elif tool_name == "graph.run_readonly_cypher":
                query_str = arguments.get("query")
                if not query_str:
                    return {"status": "error", "error": "Missing required argument 'query'"}
                params = arguments.get("params", {})
                rows = self.graph.query(query_str, params=params)
                return {"status": "ok", "result": rows}

            elif tool_name == "algo.score_risk":
                account_id = arguments.get("account_id")
                if not account_id:
                    return {"status": "error", "error": "Missing required argument 'account_id'"}
                result = compute_risk_score(self.graph, account_id)
                return {"status": "ok", "result": result}

            elif tool_name == "action.create_case":
                title = arguments.get("title", "Investigation Case")
                entity_ids = arguments.get("entity_ids", [])
                summary = arguments.get("summary", "")
                case_id = self.action_service.create_case(title, entity_ids, summary)
                return {"status": "ok", "result": {"case_id": case_id}}

            elif tool_name == "action.flag_entity":
                case_id = arguments.get("case_id", "")
                entity_id = arguments.get("entity_id", "")
                reason = arguments.get("reason", "")
                evidence_ids = arguments.get("evidence_ids", [])
                record = self.action_service.flag_entity(case_id, entity_id, reason, evidence_ids)
                return {"status": "ok", "result": record}

            elif tool_name == "action.freeze_account":
                case_id = arguments.get("case_id", "")
                account_id = arguments.get("account_id", "")
                reason = arguments.get("reason", "")
                evidence_ids = arguments.get("evidence_ids", [])
                record = self.action_service.freeze_account(case_id, account_id, reason, evidence_ids)
                return {"status": "ok", "result": record}

            elif tool_name == "action.block_device":
                case_id = arguments.get("case_id", "")
                device_id = arguments.get("device_id", "")
                reason = arguments.get("reason", "")
                evidence_ids = arguments.get("evidence_ids", [])
                record = self.action_service.block_device(case_id, device_id, reason, evidence_ids)
                return {"status": "ok", "result": record}

            elif tool_name == "action.approve_action":
                action_id = arguments.get("action_id", "")
                approver_id = arguments.get("approver_id", "")
                record = self.action_service.approve_action(action_id, approver_id)
                return {"status": "ok", "result": record}

            return {"status": "error", "error": f"Unknown tool '{tool_name}'"}

        except ValueError as ve:
            return {"status": "error", "error": str(ve)}
        except Exception as ex:
            return {"status": "error", "error": f"Internal tool failure: {str(ex)}"}
