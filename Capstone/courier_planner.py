"""
Mini-Courier Planner  --  DAA Capstone (ETCCDA302)

Pipeline:
  1. Merge Sort          -> order parcels by deadline, then priority
  2. 0/1 Knapsack (DP)   -> choose the most valuable parcels that fit in the van
  3. Dijkstra            -> shortest path between any two delivery points
  4. Nearest-Neighbor    -> approximate TSP tour over the chosen destinations
  5. Performance testing -> runtime of each stage for growing input sizes

Run:  python courier_planner.py            (demo on sample_data.json)
      python courier_planner.py --perf     (runtime tests + chart)
"""

import heapq
import json
import random
import sys
import time

# --------------------------------------------------------------------------
# DATA DESIGN
# --------------------------------------------------------------------------
# Parcel   : dict(id, dest, weight, priority, deadline)
#              dest     -> node number in the graph (0 is the depot)
#              weight   -> kg, used as knapsack weight
#              priority -> 1..10, used as knapsack value
#              deadline -> hours from now, used for sorting
# Graph    : adjacency list  {node: [(neighbor, distance_km), ...]}  (undirected)


# --------------------------------------------------------------------------
# PHASE 2a: MERGE SORT   O(n log n) time, O(n) space, stable
# --------------------------------------------------------------------------
def sort_key(p):
    """Earlier deadline first; on a tie, higher priority first."""
    return (p["deadline"], -p["priority"])


def merge_sort(parcels):
    if len(parcels) <= 1:
        return parcels
    mid = len(parcels) // 2
    left = merge_sort(parcels[:mid])
    right = merge_sort(parcels[mid:])
    return _merge(left, right)


def _merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if sort_key(left[i]) <= sort_key(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# --------------------------------------------------------------------------
# PHASE 2b: 0/1 KNAPSACK (Dynamic Programming)   O(n*W) time and space
# --------------------------------------------------------------------------
def knapsack(parcels, capacity):
    """
    dp[i][w] = best total priority using the first i parcels with weight limit w.
    Returns (best_value, chosen_parcels, dp_table).
    Weights must be integers (kg).
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt, val = parcels[i - 1]["weight"], parcels[i - 1]["priority"]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]                       # skip parcel i
            if wt <= w:                                   # or take parcel i
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)

    # backtrack to find WHICH parcels were chosen
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            chosen.append(parcels[i - 1])
            w -= parcels[i - 1]["weight"]
    chosen.reverse()
    return dp[n][capacity], chosen, dp


# --------------------------------------------------------------------------
# PHASE 3a: DIJKSTRA   O((V + E) log V) with a binary heap
# --------------------------------------------------------------------------
def dijkstra(graph, source):
    """Returns (dist, prev). prev lets us rebuild the actual path."""
    dist = {v: float("inf") for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                                      # stale entry
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def build_path(prev, target):
    path = []
    while target is not None:
        path.append(target)
        target = prev[target]
    return path[::-1]


# --------------------------------------------------------------------------
# PHASE 3b: NEAREST-NEIGHBOR TSP APPROXIMATION   O(k^2) on k stops
# --------------------------------------------------------------------------
def nearest_neighbor_route(graph, depot, stops):
    """
    Greedy tour: from the current stop always go to the closest unvisited stop,
    then return to the depot. Distances come from Dijkstra on the real road graph.
    Returns (stop_order, full_node_path, total_km).
    """
    stops = set(stops) - {depot}
    cache = {}                                            # Dijkstra results per node

    def sp(src):
        if src not in cache:
            cache[src] = dijkstra(graph, src)
        return cache[src]

    current, order, full_path, total = depot, [depot], [depot], 0.0
    while stops:
        dist, prev = sp(current)
        nxt = min(stops, key=lambda s: dist[s])
        total += dist[nxt]
        full_path.extend(build_path(prev, nxt)[1:])       # skip duplicate start node
        order.append(nxt)
        stops.remove(nxt)
        current = nxt

    dist, prev = sp(current)                              # return to depot
    total += dist[depot]
    full_path.extend(build_path(prev, depot)[1:])
    order.append(depot)
    return order, full_path, total


# --------------------------------------------------------------------------
# DATA HELPERS
# --------------------------------------------------------------------------
def graph_from_edges(edges):
    g = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w))
        g.setdefault(v, []).append((u, w))
    return g


def generate_dataset(n_parcels, n_nodes, seed=1):
    """Random connected road network + random parcels (for performance tests)."""
    rnd = random.Random(seed)
    edges = [(i, i + 1, rnd.randint(2, 20)) for i in range(n_nodes - 1)]   # chain => connected
    for _ in range(n_nodes * 2):                                           # extra shortcuts
        u, v = rnd.sample(range(n_nodes), 2)
        edges.append((u, v, rnd.randint(2, 30)))
    parcels = [{"id": f"P{i+1}", "dest": rnd.randint(1, n_nodes - 1),
                "weight": rnd.randint(1, 15), "priority": rnd.randint(1, 10),
                "deadline": rnd.randint(1, 48)} for i in range(n_parcels)]
    return parcels, graph_from_edges(edges)


def load_dataset(path):
    with open(path) as f:
        data = json.load(f)
    return data["parcels"], graph_from_edges(data["edges"]), data["capacity"], data["depot"]


# --------------------------------------------------------------------------
# FULL PIPELINE
# --------------------------------------------------------------------------
def plan_delivery(parcels, graph, capacity, depot=0, verbose=False):
    t = {}

    t0 = time.perf_counter()
    sorted_parcels = merge_sort(parcels)
    t["sort"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    best, chosen, dp = knapsack(sorted_parcels, capacity)
    t["knapsack"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    stops = [p["dest"] for p in chosen]
    order, path, total = nearest_neighbor_route(graph, depot, stops)
    t["route"] = time.perf_counter() - t0

    result = dict(sorted=sorted_parcels, best_value=best, chosen=chosen,
                  order=order, path=path, total_km=total, times=t, dp=dp)
    if verbose:
        print_report(result, capacity)
    return result


def print_report(r, capacity):
    print("=" * 62)
    print("STEP 1: Parcels sorted by deadline (then priority)")
    print(f"  {'ID':<5}{'Dest':<6}{'Wt(kg)':<8}{'Prio':<6}{'Deadline(h)'}")
    for p in r["sorted"]:
        print(f"  {p['id']:<5}{p['dest']:<6}{p['weight']:<8}{p['priority']:<6}{p['deadline']}")

    print("\nSTEP 2: Knapsack (van capacity = %d kg)" % capacity)
    print("  Best total priority :", r["best_value"])
    print("  Parcels loaded      :", [p["id"] for p in r["chosen"]])
    print("  Total weight        :", sum(p["weight"] for p in r["chosen"]), "kg")
    left = [p["id"] for p in r["sorted"] if p not in r["chosen"]]
    print("  Left for next trip  :", left)

    print("\nSTEP 3: Route (Dijkstra + Nearest-Neighbor TSP)")
    print("  Stop order  :", " -> ".join(map(str, r["order"])))
    print("  Full path   :", " -> ".join(map(str, r["path"])))
    print("  Total length: %.1f km" % r["total_km"])

    print("\nRUNTIME (seconds)")
    for k, v in r["times"].items():
        print(f"  {k:<10}{v:.6f}")
    print("=" * 62)


# --------------------------------------------------------------------------
# PHASE 4: PERFORMANCE TESTING
# --------------------------------------------------------------------------
def bubble_sort(parcels):
    """Slow baseline O(n^2) used only to compare against merge sort."""
    a = parcels[:]
    for i in range(len(a)):
        for j in range(len(a) - i - 1):
            if sort_key(a[j]) > sort_key(a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def correctness_checks():
    parcels, graph = generate_dataset(40, 30, seed=7)
    assert merge_sort(parcels) == sorted(parcels, key=sort_key), "merge sort mismatch"
    assert merge_sort(parcels) == bubble_sort(parcels), "bubble sort mismatch"

    # brute-force check of knapsack on a small instance
    small = parcels[:12]
    best, chosen, _ = knapsack(small, 30)
    brute = 0
    for mask in range(1 << len(small)):
        w = v = 0
        for i in range(len(small)):
            if mask >> i & 1:
                w += small[i]["weight"]; v += small[i]["priority"]
        if w <= 30:
            brute = max(brute, v)
    assert best == brute, "knapsack not optimal"
    assert sum(p["weight"] for p in chosen) <= 30

    # Dijkstra on a tiny known graph
    g = graph_from_edges([(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 5)])
    d, _ = dijkstra(g, 0)
    assert d[1] == 3 and d[3] == 8, "dijkstra wrong"
    print("All correctness checks passed (merge sort, knapsack vs brute force, Dijkstra).")


def performance_test(sizes=(10, 50, 100, 200, 500, 1000), capacity=100):
    rows = []
    for n in sizes:
        parcels, graph = generate_dataset(n, max(20, n // 2), seed=n)
        r = plan_delivery(parcels, graph, capacity)
        t0 = time.perf_counter(); bubble_sort(parcels); bub = time.perf_counter() - t0
        rows.append((n, r["times"]["sort"], bub, r["times"]["knapsack"], r["times"]["route"],
                     len(r["chosen"]), r["total_km"]))
    print(f"\n{'n':>6}{'merge':>10}{'bubble':>10}{'knapsack':>11}{'route':>10}{'loaded':>8}{'km':>9}")
    for n, m, b, k, rt, c, km in rows:
        print(f"{n:>6}{m:>10.5f}{b:>10.5f}{k:>11.5f}{rt:>10.5f}{c:>8}{km:>9.1f}")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        ns = [r[0] for r in rows]
        fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
        ax[0].plot(ns, [r[1] for r in rows], "o-", label="Merge sort  O(n log n)")
        ax[0].plot(ns, [r[2] for r in rows], "s-", label="Bubble sort  O(n²)")
        ax[0].set(title="Sorting: merge vs bubble", xlabel="Number of parcels", ylabel="Time (s)")
        ax[0].legend(); ax[0].grid(alpha=.3)
        ax[1].plot(ns, [r[1] for r in rows], "o-", label="Sort")
        ax[1].plot(ns, [r[3] for r in rows], "s-", label="Knapsack DP  O(nW)")
        ax[1].plot(ns, [r[4] for r in rows], "^-", label="Dijkstra + NN-TSP")
        ax[1].set(title="Runtime of major pipeline steps", xlabel="Number of parcels", ylabel="Time (s)")
        ax[1].legend(); ax[1].grid(alpha=.3)
        plt.tight_layout()
        plt.savefig("runtime_chart.png", dpi=150)
        print("Saved runtime_chart.png")
    except ImportError:
        print("matplotlib not installed: run `pip install matplotlib` to get the chart.")


# --------------------------------------------------------------------------
if __name__ == "__main__":
    if "--perf" in sys.argv:
        correctness_checks()
        performance_test()
    else:
        parcels, graph, capacity, depot = load_dataset("sample_data.json")
        plan_delivery(parcels, graph, capacity, depot, verbose=True)
