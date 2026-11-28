# Lab Question 2.6: Longest Common Subsequence (LCS) Analysis

def analyze_longest_common_subsequence(first, second):
    m = len(first)
    n = len(second)

    # DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct LCS
    i = m
    j = n
    lcs = []

    while i > 0 and j > 0:
        if first[i - 1] == second[j - 1]:
            lcs.append(first[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs.reverse()
    lcs_string = ''.join(lcs)

    if lcs_string == "":
        lcs_string = "None"

    result = []

    result.append("LCS Analysis Report")
    result.append(f"First String Length: {m}")
    result.append(f"Second String Length: {n}")
    result.append(f"LCS Length: {dp[m][n]}")
    result.append(f"LCS String: {lcs_string}")
    result.append(f"DP Table Size: {m + 1} x {n + 1}")
    result.append(f"DP Cell Computations: {m * n}")
    result.append("Time Complexity: O(m*n)")
    result.append("Space Complexity: O(m*n)")
    result.append(
        "Observation: Dynamic Programming avoids repeated subsequence calculations"
    )

    return result

# Lab Question 2.7: Optimization Technique Reflection

def generate_optimization_reflection_report(scenarios):
    
    recommendations = {
        "TASK_SORTING": (
            "Divide-and-Conquer",
            "Problem can be divided and combined"
        ),

        "MEETING_SCHEDULE": (
            "Greedy",
            "Earliest finish time maximizes compatible activities"
        ),

        "RESOURCE_FRACTION": (
            "Greedy",
            "Highest ratio choice gives optimal fractional result"
        ),

        "JOB_PROFIT": (
            "Greedy",
            "Highest profit job is placed before deadline"
        ),

        "ZERO_ONE_KNAPSACK": (
            "Dynamic Programming",
            "Complete item choices require optimal subproblem table"
        ),

        "SEQUENCE_MATCHING": (
            "Dynamic Programming",
            "Overlapping subsequences are reused"
        )
    }

    result = []

    result.append("Optimization Technique Reflection Report")

    result.append("Technique Comparison")
    result.append("Technique BestUsedFor Limitation Example")

    result.append(
        "Divide-and-Conquer Large independent subproblems "
        "Extra merging or partition overhead Merge Sort and Quick Sort"
    )

    result.append(
        "Greedy Locally optimal choices "
        "May not always give global optimum Activity Selection and Fractional Knapsack"
    )

    result.append(
        "Dynamic Programming Overlapping subproblems "
        "Requires more memory 0/1 Knapsack and LCS"
    )

    result.append("Scenario Recommendations")
    result.append("Scenario Technique Reason")

    for scenario in scenarios:
        technique, reason = recommendations[scenario]
        result.append(f"{scenario} {technique} {reason}")

    result.append("Summary")
    result.append(
        "Most Reliable for Exact Optimization: Dynamic Programming"
    )
    result.append(
        "Fastest for Simple Scheduling Decisions: Greedy"
    )
    result.append(
        "Best for Sorting Large Data: Divide-and-Conquer"
    )
    result.append(
        "Conclusion: Algorithm choice depends on problem structure and constraints"
    )

    return result