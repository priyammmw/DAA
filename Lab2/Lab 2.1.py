# Lab Question 2.1: Task Prioritization

def compare_merge_quick_tasks(tasks):
    def comes_before(a, b):
        return (a[1], b[0]) > (b[1], a[0])

    m_count, q_count = 0, 0

    def merge_sort(arr):
        nonlocal m_count
        if len(arr) <= 1: return arr
        mid = len(arr) // 2
        l, r = merge_sort(arr[:mid]), merge_sort(arr[mid:])
        res, i, j = [], 0, 0
        while i < len(l) and j < len(r):
            m_count += 1
            if comes_before(l[i], r[j]):
                res.append(l[i]); i += 1
            else:
                res.append(r[j]); j += 1
        return res + l[i:] + r[j:]

    def quick_sort(arr):
        nonlocal q_count
        if len(arr) <= 1: return arr
        p = arr[-1]
        l, r = [], []
        for x in arr[:-1]:
            q_count += 1
            (l if comes_before(x, p) else r).append(x)
        return quick_sort(l) + [p] + quick_sort(r)

    m_res, q_res = merge_sort(tasks), quick_sort(tasks)
    m_str = [f"{t[0]} {t[1]}" for t in m_res]
    q_str = [f"{t[0]} {t[1]}" for t in q_res]

    better = "Better Algorithm: Merge Sort" if m_count < q_count else \
             "Better Algorithm: Quick Sort" if q_count < m_count else "Both Equal."

    return ["Task Prioritization Report", "Merge Sort Result"] + m_str + \
           [f"Merge Comparisons: {m_count}", "Quick Sort Result"] + q_str + \
           [f"Quick Comparisons: {q_count}", better]