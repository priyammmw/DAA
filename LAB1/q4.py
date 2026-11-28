import math

def generate_execution_observation_table(sizes):
    
    print("Algorithm Execution Observation Table")

    print("InputSizeRecursiveFactorialIterativeFactorialRecursiveFibonacciIterativeFibonacciLinearSearchBinarySearchBubbleSortInsertionSort")

    def count_fib_calls(n):
        if n <= 1:
            return 1
        return 1 + count_fib_calls(n - 1) + count_fib_calls(n - 2)

    for n in sizes:
        rec_fact = n + 1
        iter_fact = n
        rec_fib = count_fib_calls(n)
        iter_fib = n
        lin_search = n
        bin_search = math.floor(math.log2(n)) + 1 if n > 0 else 0
        bubble_sort = (n * (n - 1)) // 2
        insertion_sort = (n * (n - 1)) // 2
        
        
        row = f"{n}{rec_fact}{iter_fact}{rec_fib}{iter_fib}{lin_search}{bin_search}{bubble_sort}{insertion_sort}"
        print(row)