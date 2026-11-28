# Lab Question 3.3: Dijkstra's Shortest Path Report

def dijkstra_shortest_path_report(n, edges, source):
    adj = {i: [] for i in range(1, n + 1)}

    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    distances = {i: float('inf') for i in range(1, n + 1)}
    paths = {i: [] for i in range(1, n + 1)}

    distances[source] = 0
    paths[source] = [source]

    visited = set()

    for _ in range(n):
        u = -1
        min_dist = float('inf')

        for i in range(1, n + 1):
            if i not in visited and distances[i] < min_dist:
                min_dist = distances[i]
                u = i

        if u == -1:
            break

        visited.add(u)

        for v, w in adj[u]:
            if v not in visited:
                new_dist = distances[u] + w

                if new_dist < distances[v]:
                    distances[v] = new_dist
                    paths[v] = paths[u] + [v]

    result = []

    result.append("Dijkstra Shortest Path Report")
    result.append(f"Vertices: {n}")
    result.append(f"Edges: {len(edges)}")
    result.append(f"Source Vertex: {source}")
    result.append("Shortest Paths")
    result.append("Vertex Distance Path")

    for i in range(1, n + 1):
        if distances[i] == float('inf'):
            result.append(f"{i} INF None")
        else:
            path_str = "->".join(map(str, paths[i]))
            result.append(f"{i} {distances[i]} {path_str}")

    result.append("Complexity: O(V^2 + E)")
    result.append(
        "Observation: Dijkstra selects the nearest unvisited vertex and relaxes outgoing edges"
    )

    return result

# Lab Question 3.4: Bellman-Ford Shortest Path Report

def bellman_ford_shortest_path_report(n, edges, source):
    distances = {i: float('inf') for i in range(1, n + 1)}
    paths = {i: [] for i in range(1, n + 1)}
    
    distances[source] = 0
    paths[source] = [source]
    
    # Relax all edges n - 1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                distances[v] = distances[u] + w
                paths[v] = paths[u] + [v]
                
    # Check for reachable negative weight cycles
    negative_cycle = False
    for u, v, w in edges:
        if distances[u] != float('inf') and distances[u] + w < distances[v]:
            negative_cycle = True
            break
            
    # Print Report Headers
    print("Bellman Ford Shortest Path Report")
    print(f"Vertices: {n}")
    print(f"Edges: {len(edges)}")
    print(f"Source Vertex: {source}")
    
    if negative_cycle:
        print("Negative Cycle: Yes")
        print("Shortest Paths")
        print("Not possible because graph contains a reachable negative weight cycle")
    else:
        print("Negative Cycle: No")
        print("Shortest Paths")
        print("Vertex Distance Path")
        for i in range(1, n + 1):
            dist_val = distances[i]
            if dist_val == float('inf'):
                dist_str = "INF"
                path_str = "None"
            else:
                dist_str = str(dist_val)
                path_str = "->".join(map(str, paths[i]))
            print(f"{i} {dist_str} {path_str} ")
            
    print("Complexity: O(V*E)")
    print("Observation: Bellman-Ford relaxes all edges and can detect negative weight cycles")
    return []