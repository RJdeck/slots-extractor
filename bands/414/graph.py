from collections import defaultdict

def get_match_length(chip1, chip2, strict_num=1):
    return min(len(chip1), len(chip2)) - strict_num

def reconstruct_array(segments):
    # 创建有向图
    graph = defaultdict(list)
    for i in range(len(segments)):
        for j in range(len(segments)):
            if i != j:
                overlap = get_match_length(segments[i], segments[j])
                if segments[i][-overlap:] == segments[j][:overlap]:
                    graph[i].append((j, overlap))

    # 记录每个节点的最长路径长度和前驱节点
    max_length = defaultdict(int)
    prev_node = {}

    # 遍历所有节点,更新最长路径长度和前驱节点
    for node in range(len(segments)):
        dfs(node, graph, max_length, prev_node, set(), segments)

    # 找到最长路径的起点
    start_node = max(max_length, key=max_length.get)

    # 重构原数组
    original_array = segments[start_node]
    current_node = start_node
    while current_node in prev_node:
        next_node, overlap = prev_node[current_node]
        original_array += segments[next_node][overlap:]
        current_node = next_node

    return original_array

def dfs(node, graph, max_length, prev_node, visited, segments):
    if node in visited:
        return 0

    visited.add(node)

    if node in max_length:
        return max_length[node]

    max_len = 0
    prev = None
    for neighbor, weight in graph[node]:
        length = dfs(neighbor, graph, max_length, prev_node, visited, segments) + weight
        if length > max_len:
            max_len = length
            prev = (neighbor, weight)

    max_length[node] = max(max_length[node], len(segments[node]) + max_len)
    if max_len > 0:
        prev_node[node] = prev

    visited.remove(node)

    return max_length[node]