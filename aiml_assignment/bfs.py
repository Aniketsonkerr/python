from collections import deque


def bfs_traversal(vertices, edges, start_vertex):
    # Construct Adjacency List for Undirected Graph
    adj = [[] for _ in range(vertices)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Data structures to track BFS execution state
    visited = [False] * vertices
    parent = [-1] * vertices
    distance = [-1] * vertices

    queue = deque([start_vertex])
    visited[start_vertex] = True
    distance[start_vertex] = 0

    visited_order = []
    iteration = 1

    print("=== Queue Trace Per Iteration ===")
    print(f"Initial Queue: {list(queue)}")

    # BFS Loop
    while queue:
        curr = queue.popleft()
        visited_order.append(curr)

        # Explore neighbors in sorted order for deterministic traversal
        for neighbor in sorted(adj[curr]):
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = curr
                distance[neighbor] = distance[curr] + 1
                queue.append(neighbor)

        print(
            f"Iteration {iteration} (Processed {curr}): Queue = {list(queue)}"
        )
        iteration += 1

    # Display Results
    print("\nBFS Traversal Order:")
    print(" → ".join(map(str, visited_order)))

    print("\nVertex\tParent\tDistance")
    for i in range(vertices):
        p = parent[i] if parent[i] != -1 else "-"
        print(f"{i}\t{p}\t{distance[i]}")


if __name__ == "__main__":
    # Graph Input Configuration: G = (V, E)
    num_vertices = 6
    edge_list = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5)]
    start = 0

    bfs_traversal(num_vertices, edge_list, start)