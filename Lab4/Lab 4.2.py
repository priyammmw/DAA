# Lab Question 4.5: Observed Runtime and Complexity Report

def analyze_observed_runtime_complexity(cases):
  output = ["Observed Runtime and Complexity Report"]
  output.append("Case Scenario Matches NaiveUnits RabinKarpUnits KMPUnits ObservedBest TheoreticalChoice")

  t_m = {
    "SIMPLE_TEXT": "Naive",
    "LONG_REPETITIVE": "KMP",
    "HASH_BASED_SEARCH": "Rabin-Karp",
  }

  def naive_search(text, pattern):
    n, m = len(text), len(pattern)
    comps = 0
    matches = []
    for i in range(n-m+1):
      matched = True
      for j in range(m):
        comps += 1
        if text[i+j] != pattern[j]:
          matched = False
          break
      if matched:
        matches.append(i)
    return matches, comps

  def rabin_karp_search(text, pattern, base=256, mod=101):
    n, m = len(text), len(pattern)
    if m > n:
      return [], 0

    pat_hash = 0
    win_hash = 0
    h = pow(base, m-1, mod)

    for i in range(m):
      pat_hash = (pat_hash * base + ord(pattern[i])) % mod
      win_hash = (win_hash * base + ord(text[i])) % mod

    units = 0
    matches = []

    for i in range(n-m+1):
      units += 1
      if win_hash == pat_hash:
        char_match = True
        for j in range(m):
          units += 1
          if text[i+j] != pattern[j]:
            char_match = False
            break
        if char_match:
          matches.append(i)

      if i < n-m:
        win_hash = ((win_hash - ord(text[i]) * h) * base + ord(text[i+m])) % mod
        if win_hash < 0:
          win_hash += mod

    return matches, units

  def build_lps(pattern):
    m = len(pattern)
    lps = [0]*m
    length = 0
    i = 1
    while i < m:
      if pattern[i] == pattern[length]:
        length += 1
        lps[i] = length
        i += 1
      else:
        if length != 0:
          length = lps[length-1] 
        else:
          lps[i] = 0
          i += 1
    return lps

  def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    lps = build_lps(pattern)
    comps = 0
    matches = []
    i = 0
    j = 0

    while i < n:
      comps += 1
      if text[i] == pattern[j]:
        i += 1
        j += 1
        if j == m:
          matches.append(i-j)
          j = lps[j-1]
      else:
        if j != 0:
          j = lps[j-1]
        else:
          i += 1

    return matches, comps

  for idx, (scenario, text, pattern) in enumerate(cases, start=1):
    naive_matches, naive_units = naive_search(text, pattern)
    rk_matches, rk_units = rabin_karp_search(text, pattern)
    kmp_matches, kmp_units = kmp_search(text, pattern)

    match_count = len(kmp_matches)
    algo_units = [
      ("Naive", naive_units),
      ("Rabin-Karp", rk_units),
      ("KMP", kmp_units),
    ]
    min_units = min(u for _, u in algo_units)
    best_algos = "+".join(name for name, u in algo_units if u == min_units)
    theo_choice = t_m.get(scenario, "Naive")

    output.append(f"{idx} {scenario} {match_count} {naive_units} {rk_units} {kmp_units} {best_algos} {theo_choice}")

  output.append("Theoretical Complexity")
  output.append("Naive: O(n*m)")
  output.append("Rabin-Karp Average: O(n+m)")
  output.append("Rabin-Karp Worst: O(n*m)")
  output.append("KMP: O(n+m)")
  output.append("Scenario Suitability")
  output.append("SIMPLE_TEXT: Naive is suitable for short and straightforward searches")

  output.append("LONG_REPETITIVE: KMP is suitable because LPS avoids repeated comparisons")

  output.append("HASH_BASED_SEARCH: Rabin-Karp is suitable for hash-based or multiple-pattern filtering")
  output.append("Conclusion: Observed runtime units depend on input structure while theoretical complexity describes growth")
    
  return output