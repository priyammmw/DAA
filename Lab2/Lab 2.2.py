# Lab Question 2.2: Activity Selection Problem

def select_meeting_activities(activities):
    # Sort by finish time, then start time, then activity ID
    activities.sort(key=lambda x: (x[2], x[1], x[0]))

    selected = []
    last_finish = -1

    for activity_id, start, finish in activities:
        if start >= last_finish:
            if len(selected) == 0:
                reason = "Selected first because it finishes earliest"
            else:
                reason = "Selected because start time is compatible"

            selected.append(
                f"{activity_id} {start} {finish} {reason}"
            )
            last_finish = finish

    result = []

    result.append("Activity Selection Report")
    result.append("Selected Activities")
    result.append("Activity Start Finish Reason")

    for activity in selected:
        result.append(activity)

    result.append(f"Total Selected: {len(selected)}")
    result.append(
        "Justification: Greedy selection by earliest finish time maximizes compatible activities"
    )

    return result

# Lab Question 2.3: Fractional Knapsack Problem
def fractional_knapsack_allocation(items, capacity):
    # Sort by highest value-to-weight ratio.
    # If ratios are equal, choose lexicographically smaller item ID.
    items.sort(key=lambda x: (-x[1] / x[2], x[0]))

    result = []
    total_profit = 0.0
    total_weight = 0.0
    remaining_capacity = float(capacity)

    result.append("Fractional Knapsack Report")
    result.append("Selected Items")
    result.append("Item Value Weight Fraction Profit")

    for item_id, value, weight in items:
        if remaining_capacity <= 0:
            break

        if weight <= remaining_capacity:
            fraction = 1.0
            used_weight = float(weight)
            profit = float(value)
        else:
            fraction = remaining_capacity / weight
            used_weight = remaining_capacity
            profit = float(value) * fraction

        total_weight += used_weight
        total_profit += profit
        remaining_capacity -= used_weight

        result.append(
            f"{item_id} {float(value):.2f} {float(weight):.2f} "
            f"{fraction:.2f} {profit:.2f}"
        )

    result.append(f"Maximum Profit: {total_profit:.2f}")
    result.append(f"Total Weight Used: {total_weight:.2f}")
    result.append(
        "Selection Strategy: Highest value-to-weight ratio first"
    )

    return result