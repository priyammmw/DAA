# Lab Question 3.5: Prim's Minimum Spanning Tree Report

def prim_minimum_spanning_tree_report(n, edges):
    visited = {1}
    mst_edges = []
    total_cost = 0

    while len(visited) < n:
        min_edge = None

        for u, v, w in edges:
            if u in visited and v not in visited:
                candidate = (w, u, v)

                if min_edge is None or candidate < min_edge:
                    min_edge = candidate

            elif v in visited and u not in visited:
                candidate = (w, v, u)

                if min_edge is None or candidate < min_edge:
                    min_edge = candidate

        if min_edge is None:
            break

        w, u, v = min_edge

        visited.add(v)
        mst_edges.append((u, v, w))
        total_cost += w

    result = []

    result.append("Prim Minimum Spanning Tree Report")
    result.append(f"Vertices: {n}")
    result.append(f"Edges: {len(edges)}")
    result.append("Start Vertex: 1")
    result.append("MST Edges")

    if len(mst_edges) == n - 1:
        result.append("From To Weight")

        for u, v, w in mst_edges:
            result.append(f"{u} {v} {w}")

        result.append(f"Total Cost: {total_cost}")
    else:
        result.append("Not possible because graph is disconnected")
        result.append("Total Cost: -1")

    result.append(f"Edges Selected: {len(mst_edges)}")
    result.append("Complexity: O(V*E)")
    result.append(
        "Observation: Prim grows the MST by repeatedly selecting the minimum crossing edge"
    )

    return result

# Lab Question 3.6: Graph Algorithm Complexity Analysis

def analyze_graph_algorithm_complexity(cases):
    result = []

    result.append("Graph Algorithm Complexity Report")
    result.append("Case Analysis")
    result.append(
        "Case Vertices Edges NegativeEdges GraphType MatrixSpace "
        "ListSpace DijkstraCount BellmanFordCount PrimCount "
        "ShortestPathChoice RepresentationChoice"
    )

    for i, case in enumerate(cases, 1):
        v, e, negative = case

        if isinstance(negative, bool):
            negative = "Yes" if negative else "No"
        else:
            negative = str(negative).capitalize()

        matrix_space = v * v
        list_space = v + 2 * e

        dijkstra_count = v * v + e
        bellman_ford_count = v * e
        prim_count = v * e

        max_edges = v * (v - 1) // 2

        if e <= max_edges / 2:
            graph_type = "Sparse"
            representation = "AdjacencyList"
        else:
            graph_type = "Dense"
            representation = "AdjacencyMatrix"

        if negative == "Yes":
            shortest_path = "Bellman-Ford"
        else:
            shortest_path = "Dijkstra"

        row = (
            f"{i} {v} {e} {negative} {graph_type} "
            f"{matrix_space} {list_space} "
            f"{dijkstra_count} {bellman_ford_count} "
            f"{prim_count} {shortest_path} {representation}"
        )

        result.append(row)

    result.append("Complexity Summary")
    result.append("Dijkstra: O(V^2 + E)")
    result.append("Bellman-Ford: O(V*E)")
    result.append("Prim: O(V*E)")
    result.append("Adjacency Matrix Space: O(V^2)")
    result.append("Adjacency List Space: O(V+E)")
    result.append(
        "Observation: Algorithm choice depends on edge weights, "
        "graph density and optimization goal"
    )

    return result