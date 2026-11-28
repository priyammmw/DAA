# Lab Question 2.4: Knapsack Comparison

def knapsack_comparison(items, capacity):
    # 0/1 Knapsack using Dynamic Programming
    n = len(items)

    # dp[w] = maximum value for capacity w
    dp = [0] * (capacity + 1)

    # Keep track of selected items
    selected_01 = [[] for _ in range(capacity + 1)]

    for i, (item_id, value, weight) in enumerate(items):
        for w in range(capacity, weight - 1, -1):
            new_value = dp[w - weight] + value

            if new_value > dp[w]:
                dp[w] = new_value
                selected_01[w] = selected_01[w - weight] + [i]

    selected_indices = selected_01[capacity]

    # Display 0/1 items in original input order
    selected_indices.sort()

    value_01 = sum(items[i][1] for i in selected_indices)
    weight_01 = sum(items[i][2] for i in selected_indices)

    # Fractional Knapsack - sort by value/weight ratio
    fractional_items = sorted(
        range(n),
        key=lambda i: (-items[i][1] / items[i][2], items[i][0])
    )

    remaining = capacity
    fractional_selected = []
    fractional_profit = 0.0
    fractional_weight = 0.0

    for i in fractional_items:
        item_id, value, weight = items[i]

        if remaining <= 0:
            break

        fraction = min(1.0, remaining / weight)
        profit = value * fraction
        used_weight = weight * fraction

        fractional_selected.append(
            (item_id, value, weight, fraction, profit)
        )

        fractional_profit += profit
        fractional_weight += used_weight
        remaining -= used_weight

    difference = fractional_profit - value_01

    # Build required output
    result = []

    result.append("Knapsack Comparison Report")

    # 0/1 Knapsack
    result.append("0/1 Knapsack")
    result.append("Selected Items")
    result.append("Item Value Weight")

    for i in selected_indices:
        item_id, value, weight = items[i]
        result.append(f"{item_id} {value} {weight}")

    result.append(f"Maximum Value: {value_01}")
    result.append(f"Total Weight: {weight_01}")

    # Fractional Knapsack
    result.append("Fractional Knapsack")
    result.append("Selected Items")
    result.append("Item Value Weight Fraction Profit")

    for item_id, value, weight, fraction, profit in fractional_selected:
        result.append(
            f"{item_id} {value:.2f} {weight:.2f} "
            f"{fraction:.2f} {profit:.2f}"
        )

    result.append(f"Maximum Profit: {fractional_profit:.2f}")
    result.append(f"Total Weight: {fractional_weight:.2f}")

    # Comparison
    result.append("Comparison")
    result.append(f"Difference: {difference:.2f}")

    if fractional_profit > value_01:
        better = "Fractional Knapsack"
    elif value_01 > fractional_profit:
        better = "0/1 Knapsack"
    else:
        better = "Both Equal"

    result.append(f"Better Result: {better}")

    result.append(
        "Justification: Fractional Knapsack can take item fractions, "
        "while 0/1 Knapsack selects complete items only"
    )

    return result

# Lab Question 2.5: Job Sequencing with Deadlines

def job_sequencing_deadlines(jobs):
    # Sort jobs by:
    # 1. Descending profit
    # 2. Smaller deadline
    # 3. Lexicographically smaller job ID
    jobs = sorted(
        jobs,
        key=lambda x: (-x[2], x[1], x[0])
    )

    # Find maximum deadline
    max_deadline = max(job[1] for job in jobs)

    # Slots: index represents the time slot
    slots = [None] * (max_deadline + 1)