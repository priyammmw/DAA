def analyze_recursive_iterative(n):
  fact_val = 1
  for i in range(1, n + 1):
    fact_val *= i

  if n == 0:
    fib_val = 0
  elif n == 1:
    fib_val = 1
  else:
    a, b = 0, 1
    for _ in range (2, n + 1):
      a,b = b, a + b
    fib_val = b

  rec_fact_count = n + 1
  iter_fact_count = n

  def count_fib_calls(k):
    if k == 0 or k == 1:
      return 1
    return 1 + count_fib_calls(k - 1) + count_fib_calls(k - 2)

  rec_fib_count = count_fib_calls(n)
  iter_fib_count = n 
      
  return [
    "Computation Analysis Report\n"
    f"Recursive Factorial: {fact_val}",
    f"Iterative Factorial: {fact_val}",
    f"Recursive Fibonacci: {fib_val}",
    f"Iterative Fibonacci: {fib_val}",
    "Operation Count Comparison\n"
    f"Recursive Factorial Count: {rec_fact_count}",
    f"Iterative Factorial Count: {iter_fact_count}",
    f"Recursive Fibonacci Count: {rec_fib_count}",
    f"Iterative Fibonacci Count: {iter_fib_count}"
   
 ]