import heapq


def dijkstra(graph, start, end):
    """
    使用 Dijkstra 算法计算从 start 到 end 的最短路径。
    :param graph: 图的邻接矩阵表示
    :param start: 起始节点
    :param end: 目标节点
    :return: 最短路径上的节点序列
    """
    # 初始化距离字典和前驱节点字典
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    queue = []
    heapq.heappush(queue, (0, start))

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    # 构建最短路径
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    path = path[::-1]

    return path


def get_shortest_path(speeds, edgenode_count, start, end):
    # 剔除值为 0 的项
    speeds_remove_zero = {key: value for key,
                          value in speeds.items() if value != 0}

    # 将传输速率的倒数作为边的权重
    speeds_cost = {(i, j): 1 / rate for (i, j),
                   rate in speeds_remove_zero.items()}

    # 将 cost_uovk 转换为邻接列表形式
    adjacency_list = {i: {} for i in range(edgenode_count)}
    for (i, j), cost in speeds_cost.items():
        adjacency_list[i][j] = cost

    # 计算最短路径
    return dijkstra(adjacency_list, start, end)


if __name__ == "__main__":
    # 测试数据
    r_uovk = {
        (0, 1): 10,
        (0, 2): 5,
        (0, 3): 0,  # 不可达的情况
        (1, 2): 8,
        (1, 3): 6,
        (2, 3): 7
    }
    edgenode_count = 4

    # 计算从节点 0 到节点 3 的最短路径
    shortest_path = get_shortest_path(r_uovk, edgenode_count, 0, 3)

    print("最短路径:", shortest_path)
