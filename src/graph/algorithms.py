"""Graph algorithms: community detection, PageRank centrality, cycle detection, pathfinding, and shared attributes."""
from collections import defaultdict, deque
from typing import Any


def detect_communities(graph: Any, subgraph_nodes: list[str] | None = None) -> dict[str, list[dict[str, Any]]]:
    """Label propagation community detection on an induced subgraph."""
    nodes = set(subgraph_nodes) if subgraph_nodes else set(graph.nodes.keys())
    if not nodes:
        return {"communities": []}

    # Build undirected adjacency among target nodes
    neighbors: dict[str, list[str]] = {nid: [] for nid in nodes}
    for e in graph.edges:
        u, v = e["source"], e["target"]
        if u in nodes and v in nodes:
            neighbors[u].append(v)
            neighbors[v].append(u)

    # Initialize each node with its own unique community label
    labels = {nid: i for i, nid in enumerate(nodes)}

    # Iterative label propagation (up to 15 iterations)
    for _ in range(15):
        changed = False
        for nid in sorted(nodes):
            nbrs = neighbors.get(nid, [])
            if not nbrs:
                continue
            # Count label frequencies among neighbors
            counts: dict[int, int] = defaultdict(int)
            for nbr in nbrs:
                counts[labels[nbr]] += 1
            max_count = max(counts.values())
            # Deterministically choose minimum label among ties
            best_label = min(lbl for lbl, count in counts.items() if count == max_count)
            if best_label != labels[nid]:
                labels[nid] = best_label
                changed = True
        if not changed:
            break

    # Group nodes by community label
    community_groups: dict[int, list[str]] = defaultdict(list)
    for nid, lbl in labels.items():
        community_groups[lbl].append(nid)

    sorted_communities = []
    for cid, members in sorted(community_groups.items(), key=lambda x: len(x[1]), reverse=True):
        sorted_communities.append({
            "community_id": cid,
            "members": sorted(members),
            "size": len(members)
        })

    return {"communities": sorted_communities}


def rank_centrality(
    graph: Any,
    subgraph_nodes: list[str] | None = None,
    damping_factor: float = 0.85,
    max_iter: int = 20,
    top_k: int = 10
) -> dict[str, list[dict[str, Any]]]:
    """Computes PageRank centrality over directed edges."""
    nodes = sorted(list(subgraph_nodes if subgraph_nodes else graph.nodes.keys()))
    num_nodes = len(nodes)
    if num_nodes == 0:
        return {"rankings": []}

    # Build out-edges and in-edges restricted to the node set
    out_edges: dict[str, list[str]] = {nid: [] for nid in nodes}
    node_set = set(nodes)
    for e in graph.edges:
        u, v = e["source"], e["target"]
        if u in node_set and v in node_set:
            out_edges[u].append(v)

    # Initial uniform score distribution
    scores = {nid: 1.0 / num_nodes for nid in nodes}

    for _ in range(max_iter):
        next_scores = {nid: (1.0 - damping_factor) / num_nodes for nid in nodes}
        for u in nodes:
            successors = out_edges[u]
            if successors:
                share = (damping_factor * scores[u]) / len(successors)
                for v in successors:
                    next_scores[v] += share
            else:
                # Dangling node redistribution
                dangling_share = (damping_factor * scores[u]) / num_nodes
                for v in nodes:
                    next_scores[v] += dangling_share
        scores = next_scores

    rankings = [
        {"id": nid, "score": round(scores[nid], 4)}
        for nid in sorted(nodes, key=lambda x: scores[x], reverse=True)
    ]

    return {"rankings": rankings[:top_k]}


def detect_cycles(
    graph: Any,
    start_node: str | None = None,
    min_length: int = 3,
    max_length: int = 6
) -> dict[str, list[dict[str, Any]]]:
    """Detects simple directed cycles of length between min_length and max_length on TRANSFERRED_TO edges."""
    # Build transfer edge adjacency with amounts
    adj: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for e in graph.edges:
        if e.get("type") == "TRANSFERRED_TO":
            amount = float(e.get("properties", {}).get("amount", 0.0))
            adj[e["source"]].append((e["target"], amount))

    target_nodes = [start_node] if start_node and start_node in graph.nodes else list(graph.nodes.keys())
    found_cycles = []
    seen_canonical = set()

    for root in target_nodes:
        def dfs(curr: str, path: list[str], amount_sum: float):
            if len(path) > max_length:
                return
            for nxt, amt in adj.get(curr, []):
                if nxt == root and len(path) >= min_length:
                    # Found cycle
                    full_cycle = path + [root]
                    # Create canonical representation by rotating to minimum element
                    cycle_nodes = full_cycle[:-1]
                    min_idx = cycle_nodes.index(min(cycle_nodes))
                    canon = tuple(cycle_nodes[min_idx:] + cycle_nodes[:min_idx])
                    if canon not in seen_canonical:
                        seen_canonical.add(canon)
                        found_cycles.append({
                            "path": full_cycle,
                            "length": len(path),
                            "total_amount": amount_sum + amt
                        })
                elif nxt not in path:
                    dfs(nxt, path + [nxt], amount_sum + amt)

        dfs(root, [root], 0.0)

    return {"cycles": found_cycles}


def find_paths(
    graph: Any,
    source_id: str,
    target_id: str,
    max_hops: int = 4
) -> dict[str, Any]:
    """Finds the shortest directed/undirected relationship path between two entities via BFS."""
    if source_id not in graph.nodes or target_id not in graph.nodes:
        return {"found": False, "path": [], "hops": 0, "edges": []}

    if source_id == target_id:
        return {"found": True, "path": [source_id], "hops": 0, "edges": []}

    queue = deque([(source_id, [source_id], [])])
    visited = {source_id}

    while queue:
        curr, path, edge_path = queue.popleft()
        if len(path) - 1 >= max_hops:
            continue

        # Look through all outgoing and incoming edges
        neighbors: list[tuple[str, dict[str, Any]]] = []
        for e in graph.adj_out.get(curr, []):
            neighbors.append((e["target"], e))
        for e in graph.adj_in.get(curr, []):
            neighbors.append((e["source"], e))

        for nxt, edge_info in neighbors:
            new_path = path + [nxt]
            new_edges = edge_path + [edge_info]
            if nxt == target_id:
                return {
                    "found": True,
                    "path": new_path,
                    "hops": len(new_path) - 1,
                    "edges": new_edges
                }
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, new_path, new_edges))

    return {"found": False, "path": [], "hops": 0, "edges": []}


def find_shared_attributes(
    graph: Any,
    entity_id: str,
    attribute_type: str = "Device"
) -> dict[str, list[dict[str, Any]]]:
    """Finds accounts that share a specified attribute entity (Device, IP, Phone, Address)."""
    if entity_id not in graph.nodes:
        return {"shared_entities": []}

    # Step 1: Find connected attribute nodes
    attribute_nodes = set()
    for e in graph.adj_out.get(entity_id, []):
        tgt = e["target"]
        tgt_node = graph.nodes.get(tgt)
        if tgt_node and attribute_type in tgt_node.get("labels", []):
            attribute_nodes.add(tgt)
    for e in graph.adj_in.get(entity_id, []):
        src = e["source"]
        src_node = graph.nodes.get(src)
        if src_node and attribute_type in src_node.get("labels", []):
            attribute_nodes.add(src)

    # Step 2: For each attribute node, find all other linked entities
    shared_list = []
    for attr_id in sorted(attribute_nodes):
        linked = set()
        for e in graph.adj_in.get(attr_id, []):
            if e["source"] != entity_id and "Account" in graph.nodes.get(e["source"], {}).get("labels", []):
                linked.add(e["source"])
        for e in graph.adj_out.get(attr_id, []):
            if e["target"] != entity_id and "Account" in graph.nodes.get(e["target"], {}).get("labels", []):
                linked.add(e["target"])

        shared_list.append({
            "attribute_id": attr_id,
            "attribute_type": attribute_type,
            "linked_entities": sorted(list(linked))
        })

    return {"shared_entities": shared_list}
