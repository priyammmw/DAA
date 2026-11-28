# Lab Question 3.1: N Queens Backtracking

def solve_n_queens_backtracking(n):
    board = [-1] * n

    def is_safe(row, col):
        for r in range(row):
            c = board[r]

            if c == col:
                return False

            if abs(r - row) == abs(c - col):
                return False

        return True

    def solve(row):
        if row == n:
            return True

        for col in range(n):
            if is_safe(row, col):
                board[row] = col

                if solve(row + 1):
                    return True

                board[row] = -1

        return False

    found = solve(0)

    result = [
        "N Queens Backtracking Report",
        f"Board Size: {n}",
        f"Solution Found: {'Yes' if found else 'No'}"
    ]

    if found:
        result.append("Board")

        for r in range(n):
            result.append(" ".join(
                "Q" if board[r] == c else "."
                for c in range(n)
            ))

        result.append("Queen Positions")
        result.append("Row Column")

        for r in range(n):
            result.append(f"{r + 1} {board[r] + 1}")

    else:
        result.append("Board")
        result.append("No valid board arrangement")
        result.append("Queen Positions")
        result.append("None")

    result.append("Complexity: O(N!)")
    result.append(
        "Observation: Backtracking places queens row by row and removes unsafe choices"
    )

    return result

# Lab Question 3.2: Graph Representation

def represent_graph_matrix_list(n, edges):
    matrix = [[0] * n for _ in range(n)]
    adj_list = [[] for _ in range(n)]

    for u, v in edges:
        matrix[u - 1][v - 1] = 1
        matrix[v - 1][u - 1] = 1

        adj_list[u - 1].append(v)
        adj_list[v - 1].append(u)

    for i in range(n):
        adj_list[i].sort()

    m = len(edges)

    matrix_space = n * n
    list_space = n + 2 * m

    max_edges = n * (n - 1) // 2

    if m <= max_edges / 2:
        graph_type = "Sparse"
        recommendation = "Adjacency List"
        observation = "Adjacency List is space efficient for sparse graphs"
    else:
        graph_type = "Dense"
        recommendation = "Adjacency Matrix"
        observation = "Adjacency Matrix is suitable for dense graphs"

    result = []

    result.append("Graph Representation Report")
    result.append(f"Vertices: {n}")
    result.append(f"Edges: {m}")

    result.append("Adjacency Matrix")

    for row in matrix:
        result.append(" ".join(map(str, row)))

    result.append("Adjacency List")

    for i in range(n):
        if adj_list[i]:
            result.append(f"{i + 1}: {' '.join(map(str, adj_list[i]))}")
        else:
            result.append(f"{i + 1}: None")

    result.append("Space Comparison")
    result.append(f"Matrix Space Units: {matrix_space}")
    result.append(f"List Space Units: {list_space}")
    result.append(f"Graph Type: {graph_type}")
    result.append(f"Recommended Representation: {recommendation}")
    result.append(f"Observation: {observation}")

    return result