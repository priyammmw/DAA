def generate_runtime_chart_report(input_sizes):
    import math

    result = []

    result.append("Runtime Comparison Chart Data")
    result.append("InputSize LinearSearch BinarySearch BubbleSort InsertionSort")

    for n in input_sizes:
        linear = n
        binary = math.floor(math.log2(n)) + 1
        bubble = n * (n - 1) // 2
        insertion = n * (n - 1) // 2

        result.append(f"{n} {linear} {binary} {bubble} {insertion}")

    result.append("Scalability Summary")
    result.append("Algorithm Complexity Scalability")
    result.append("Linear Search O(n) Moderate")
    result.append("Binary Search O(log n) Excellent")
    result.append("Bubble Sort O(n^2) Poor")
    result.append("Insertion Sort O(n^2) Poor")
    result.append("Key Observations")
    result.append("Best Algorithm: Binary Search")
    result.append("Most Expensive Algorithm: Bubble Sort")
    result.append("Conclusion: Logarithmic algorithms scale better for large inputs")

    return result