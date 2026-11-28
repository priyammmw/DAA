# Lab Question 4.1: Naive Pattern Matching Report

def naive_pattern_matching_report(text, pattern):
    n = len(text)
    m = len(pattern)

    positions = []
    comparisons = 0

    for i in range(n - m + 1):
        j = 0

        while j < m:
            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        if j == m:
            positions.append(i)

    pos = " ".join(map(str, positions)) if positions else "None"

    return [
        "Naive Pattern Matching Report",
        f"Text Length: {n}",
        f"Pattern Length: {m}",
        f"Matching Positions: {pos}",
        f"Total Matches: {len(positions)}",
        f"Character Comparisons: {comparisons}",
        "Time Complexity: O(n*m)",
        "Observation: Naive pattern matching checks every possible starting position"
    ]
    
# Lab Question 4.2: Rabin-Karp Matching Report

def rabin_karp_matching_report(text, pattern):
    n = len(text)
    m = len(pattern)

    base = 256
    modulus = 101

    h = pow(base, m - 1, modulus)

    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % modulus
        window_hash = (base * window_hash + ord(text[i])) % modulus

    positions = []
    hash_comparisons = 0
    character_comparisons = 0

    for i in range(n - m + 1):
        hash_comparisons += 1

        if pattern_hash == window_hash:
            j = 0

            while j < m:
                character_comparisons += 1

                if text[i + j] != pattern[j]:
                    break

                j += 1

            if j == m:
                positions.append(i)

        if i < n - m:
            window_hash = (
                base * (window_hash - ord(text[i]) * h)
                + ord(text[i + m])
            ) % modulus

    pos = " ".join(map(str, positions)) if positions else "None"

    return [
        "Rabin Karp Matching Report",
        f"Text Length: {n}",
        f"Pattern Length: {m}",
        f"Base: {base}",
        f"Modulus: {modulus}",
        f"Pattern Hash: {pattern_hash}",
        f"Positions: {pos}",
        f"Hash Comparisons: {hash_comparisons}",
        f"Character Comparisons: {character_comparisons}",
        "Complexity",
        "Average Case: O(n+m)",
        "Worst Case: O(n*m)",
        "Observation: Rabin-Karp uses rolling hash to reduce unnecessary character matching"
    ]
    
# Lab Question 4.3: KMP Pattern Matching Report
    
def kmp_pattern_matching_report(text, pattern):
    n = len(text)
    m = len(pattern)

    lps = [0] * m
    length = 0
    i = 1

    # Construct LPS array
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        elif length != 0:
            length = lps[length - 1]

        else:
            lps[i] = 0
            i += 1

    # KMP searching
    positions = []
    comparisons = 0

    i = 0
    j = 0

    while i < n:

        while j > 0:
            comparisons += 1

            if text[i] == pattern[j]:
                break

            j = lps[j - 1]

        if j == 0:
            comparisons += 1

            if text[i] == pattern[j]:
                j += 1
        else:
            j += 1

        if j == m:
            positions.append(i - m + 1)
            j = lps[j - 1]

        i += 1

    pos = " ".join(map(str, positions)) if positions else "None"

    return [
        "KMP Pattern Matching Report",
        f"Text Length: {n}",
        f"Pattern Length: {m}",
        "LPS Array: " + " ".join(map(str, lps)),
        f"Matching Positions: {pos}",
        f"Total Matches: {len(positions)}",
        f"Character Comparisons: {comparisons}",
        "Time Complexity: O(n+m)",
        "Observation: KMP uses the LPS array to avoid unnecessary character comparisons"
    ]
    
# Lab Question 4.4: Pattern Matching Runtime Comparison Report
    
def compare_pattern_matching_runtime(cases):
    
    def naive_search(text, pattern):
        n = len(text)
        m = len(pattern)
        comparisons = 0
        matches = 0

        for i in range(n - m + 1):
            j = 0

            while j < m:
                comparisons += 1
                if text[i + j] != pattern[j]:
                    break
                j += 1

            if j == m:
                matches += 1

        return matches, comparisons

    def rabin_karp_search(text, pattern):
        n = len(text)
        m = len(pattern)

        base = 256
        modulus = 101

        h = pow(base, m - 1, modulus)

        pattern_hash = 0
        window_hash = 0

        for i in range(m):
            pattern_hash = (base * pattern_hash + ord(pattern[i])) % modulus
            window_hash = (base * window_hash + ord(text[i])) % modulus

        hash_comparisons = 0
        character_comparisons = 0
        matches = 0

        for i in range(n - m + 1):
            hash_comparisons += 1

            if pattern_hash == window_hash:
                j = 0

                while j < m:
                    character_comparisons += 1

                    if text[i + j] != pattern[j]:
                        break

                    j += 1

                if j == m:
                    matches += 1

            if i < n - m:
                window_hash = (
                    base * (window_hash - ord(text[i]) * h)
                    + ord(text[i + m])
                ) % modulus

        return matches, hash_comparisons + character_comparisons

    def kmp_search(text, pattern):
        n = len(text)
        m = len(pattern)

        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

        comparisons = 0
        matches = 0
        i = 0
        j = 0

        while i < n:
            while j > 0:
                comparisons += 1

                if text[i] == pattern[j]:
                    break

                j = lps[j - 1]

            if j == 0:
                comparisons += 1

                if text[i] == pattern[j]:
                    j += 1
            else:
                j += 1

            if j == m:
                matches += 1
                j = lps[j - 1]

            i += 1

        return matches, comparisons

    result = [
        "Pattern Matching Runtime Comparison Report",
        "Case TextLength PatternLength Matches NaiveUnits RabinKarpUnits KMPUnits BestAlgorithm"
    ]

    for index, case in enumerate(cases, start=1):

        text, pattern = case

        n = len(text)
        m = len(pattern)

        matches, naive_units = naive_search(text, pattern)

        _, rabin_units = rabin_karp_search(text, pattern)

        _, kmp_units = kmp_search(text, pattern)

        runtimes = {
            "Naive": naive_units,
            "Rabin-Karp": rabin_units,
            "KMP": kmp_units
        }

        minimum = min(runtimes.values())

        best = "+".join(
            name for name, units in runtimes.items()
            if units == minimum
        )

        result.append(
            f"{index} {n} {m} {matches} {naive_units} {rabin_units} {kmp_units} {best}"
        )

    result.extend([
        "Complexity Summary",
        "Naive: O(n*m)",
        "Rabin-Karp Average: O(n+m)",
        "Rabin-Karp Worst: O(n*m)",
        "KMP: O(n+m)",
        "Observation: Runtime performance depends on text structure, pattern length and repeated characters"
    ])

    return result