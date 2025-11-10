def find_longest_suffix(path, suffix_path):
    max_overlap = 0
    search_len = len(suffix_path)
    chain_len = len(path)
    for i in range(1, min(search_len, chain_len) + 1):
        if path[-i:] == suffix_path[:i]:
            max_overlap = i
    return suffix_path[:max_overlap]
