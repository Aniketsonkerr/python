import heapq
import json
from collections import deque
from typing import Dict, List, Tuple

# Provided 15-Node Edge Router Network JSON Data
TOPOLOGY_JSON = """{
  "network_name": "Autonomous_Edge_Cluster_Topology",
  "description": "15-Node Edge Router Network with link transmission latencies in milliseconds",
  "nodes": ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "R11", "R12", "R13", "R14"],
  "edges": [
    {"from": "R0", "to": "R1", "cost_ms": 12.5},
    {"from": "R0", "to": "R2", "cost_ms": 45.0},
    {"from": "R0", "to": "R3", "cost_ms": 16.0},
    {"from": "R1", "to": "R4", "cost_ms": 28.0},
    {"from": "R1", "to": "R5", "cost_ms": 14.2},
    {"from": "R2", "to": "R6", "cost_ms": 8.0},
    {"from": "R3", "to": "R2", "cost_ms": 10.0},
    {"from": "R3", "to": "R7", "cost_ms": 32.0},
    {"from": "R4", "to": "R8", "cost_ms": 19.5},
    {"from": "R5", "to": "R8", "cost_ms": 11.0},
    {"from": "R5", "to": "R9", "cost_ms": 26.0},
    {"from": "R6", "to": "R10", "cost_ms": 15.0},
    {"from": "R7", "to": "R10", "cost_ms": 18.5},
    {"from": "R7", "to": "R11", "cost_ms": 42.0},
    {"from": "R8", "to": "R12", "cost_ms": 22.0},
    {"from": "R9", "to": "R12", "cost_ms": 13.5},
    {"from": "R10", "to": "R13", "cost_ms": 17.0},
    {"from": "R11", "to": "R13", "cost_ms": 9.0},
    {"from": "R12", "to": "R14", "cost_ms": 16.0},
    {"from": "R13", "to": "R14", "cost_ms": 24.5},
    {"from": "R2", "to": "R5", "cost_ms": 6.5},
    {"from": "R6", "to": "R9", "cost_ms": 14.0},
    {"from": "R8", "to": "R13", "cost_ms": 30.0}
  ]
}"""


class UniformCostSearchEngine:
    def __init__(self, topology_data: dict):
        self.nodes = topology_data["nodes"]
        self.adj: Dict[str, List[Tuple[str, float]]] = {node: [] for node in self.nodes}
        for edge in topology_data["edges"]:
            u, v, w = edge["from"], edge["to"], edge["cost_ms"]
            self.adj[u].append((v, w))

    def find_optimal_path(self, source: str, destination: str) -> Tuple[List[str], float, List[str]]:
        # Priority Queue stores tuples of (cumulative_cost, current_node, path)
        pq = [(0.0, source, [source])]
        visited = set()
        expansion_trace = []

        while pq:
            cost, curr, path = heapq.heappop(pq)

            if curr in visited:
                continue

            visited.add(curr)
            expansion_trace.append(curr)

            if curr == destination:
                return path, cost, expansion_trace

            for neighbor, weight in self.adj[curr]:
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

        return [], float("inf"), expansion_trace

    def find_bfs_path(self, source: str, destination: str) -> Tuple[List[str], float, int]:
        queue = deque([(source, [source])])
        visited = {source}
        states_explored = 0

        while queue:
            curr, path = queue.popleft()
            states_explored += 1

            if curr == destination:
                # Calculate path delay post-hoc
                total_delay = 0.0
                for i in range(len(path) - 1):
                    u, v = path[i], path[i + 1]
                    for neighbor, w in self.adj[u]:
                        if neighbor == v:
                            total_delay += w
                            break
                return path, total_delay, states_explored

            for neighbor, _ in self.adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return [], float("inf"), states_explored


if __name__ == "__main__":
    topology = json.loads(TOPOLOGY_JSON)
    engine = UniformCostSearchEngine(topology)

    src, dst = "R0", "R14"

    ucs_path, ucs_cost, ucs_trace = engine.find_optimal_path(src, dst)
    bfs_path, bfs_cost, bfs_states = engine.find_bfs_path(src, dst)

    print("--- Expansion Trace (UCS Min-Heap Pop Sequence) ---")
    print(" -> ".join(ucs_trace))

    print("\n--- Route Comparisons (R0 to R14) ---")
    print(f"{'Metric':<25} | {'UCS (Optimal)':<20} | {'BFS (Unweighted)':<20}")
    print("-" * 72)
    print(f"{'Path Taken':<25} | {'->'.join(ucs_path):<20} | {'->'.join(bfs_path):<20}")
    print(f"{'Total Delay (ms)':<25} | {ucs_cost:<20.2f} | {bfs_cost:<20.2f}")
    print(f"{'Number of Hops':<25} | {len(ucs_path)-1:<20} | {len(bfs_path)-1:<20}")
    print(f"{'Total States Explored':<25} | {len(ucs_trace):<20} | {bfs_states:<20}")