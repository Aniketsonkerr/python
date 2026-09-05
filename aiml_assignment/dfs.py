def dfs_traversal(vertices, edges, start_vertex):
    # Construct Adjacency List for Undirected Graph
    adj = [[] for _ in range(vertices)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Data structures to track traversal metrics
    visited = [False] * vertices
    parent = [-1] * vertices
    discovery_time = [0] * vertices
    finish_time = [0] * vertices
    traversal_order = []

    time = 0

    def dfs_visit(u):
        nonlocal time
        time += 1
        discovery_time[u] = time
        visited[u] = True
        traversal_order.append(u)

        # Explore adjacent vertices in sorted order for deterministic trace
        for v in sorted(adj[u]):
            if not visited[v]:
                parent[v] = u
                dfs_visit(v)

        time += 1
        finish_time[u] = time

    # Execute DFS from starting vertex
    dfs_visit(start_vertex)

    # Handle disconnected components if necessary
    for i in range(vertices):
        if not visited[i]:
            dfs_visit(i)

    # Display Results
    print("DFS Traversal Order:")
    print(" → ".join(map(str, traversal_order)))

    print("\nVertex\tParent\tDiscovery\tFinish")
    for i in range(vertices):
        p = parent[i] if parent[i] != -1 else "-"
        print(f"{i}\t{p}\t{discovery_time[i]}\t\t{finish_time[i]}")


if __name__ == "__main__":
    # Graph Input Configuration: G = (V, E)
    num_vertices = 5
    edge_list = [(0, 1), (1, 2), (0, 3), (3, 4)]
    start = 0

    dfs_traversal(num_vertices, edge_list, start)