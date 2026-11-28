def compare_bubble_insertion(random_data, sorted_data, reverse_data):
  datasets = [
    ("Random Dataset", random_data),
    ("Sorted Dataset", sorted_data),
    ("Reverse Dataset", reverse_data)
  ]

  report = ["Sorting Performance Report"]

  for dataset_name, arr in datasets:
    b_arr = list(arr)
    n = len(b_arr)
    bubble_comps = 0
    bubble_swaps = 0


    for i in range(n):
      swapped = False
      for j in range(0 , n - i - 1):
        bubble_comps += 1
        if b_arr[j] > b_arr[j + 1]:
          b_arr[j], b_arr[j + 1] = b_arr[j + 1],b_arr[j]
          bubble_swaps += 1
          swapped = True
      if not swapped:
        break 

    i_arr = list(arr)
    insertion_comps = 0
    insertion_shifts = 0

    for i in range(1, len(i_arr)):
      key = i_arr[i]
      j = i - 1
      while j >= 0:
        insertion_comps += 1
        if i_arr[j] > key:
          i_arr[j + 1] = i_arr[j]
          insertion_shifts += 1
          j -= 1
        else:
          break 
      i_arr[j + 1] = key 

    if bubble_comps < insertion_comps:
      better_alg = "Bubble Sort"
    elif insertion_comps < bubble_comps:
      better_alg = "Insertion Sort"
    else:
      better_alg = "Both Equal"

    bubble_str = " ".join(map(str, b_arr))
    insertion_str = " ".join(map(str, i_arr))

    report.extend([
      dataset_name,
      f"Bubble Sorted: {bubble_str}",
      f"Bubble Comparisons: {bubble_comps}",
      f"Bubble Swaps: {bubble_swaps}",
      f"Insertion Sorted: {insertion_str}",
      f"Insertion Comparisons: {insertion_comps}",
      f"Insertion Shifts: {insertion_shifts}",
      f"Better Algorithm: {better_alg}"
                                    
    ])
   
  return report