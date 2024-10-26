from dijkstra import *


def load_sparse_graph(path: str):
    """
    读取非全连接图，返回字典
    文件示例：
    * 1 0
    * * 2
    * * *
    自己与自己直接打*
    对称阵为简化也打*
    无连接链路用0表示
    """
    with open(path, 'r') as f:
        data = {}
        line = 'sth'
        i = 0
        while line != '':
            line = f.readline()
            for j, value in enumerate(line.split()):
                if value != '*':
                    data[(i, j)] = int(value)
                    data[(j, i)] = int(value)
            i += 1
    return data


def need_reconnect(graph):
    """
    寻找需要进行连接的链路（即速率为0的链路）
    """
    need_reconnect = []
    for edge, value in graph.items():
        if value == 0:
            need_reconnect.append(edge)
    return need_reconnect


def save_graph(path: str, graph, edgenode_count: int):
    with open(path, 'w') as f:
        for i in range(edgenode_count):
            line = ''
            for j in range(edgenode_count):
                if i == j:
                    value = 0
                elif i > j:
                    value = graph[(j, i)]
                else:
                    value = graph[(i, j)]

                line += str(value) + ' '
            f.write(line.strip() + "\n")
    print(f"已保存至{path}")


if __name__ == '__main__':

    NODES = 10
    LOAD_PATH = 'graph/data/sparse2.txt'
    SAVE_PATH = 'graph/data/full2.txt'
    r_uovk = load_sparse_graph(LOAD_PATH)
    print(r_uovk)

    links = need_reconnect(r_uovk)
    print(links)

    for link in links:
        start, end = link
        shortest_path = get_shortest_path(r_uovk, NODES, start, end)
        speed = calculate_speed(shortest_path, r_uovk)
        r_uovk[link] = speed
        print(f"{start}->{end}的最短路径为{shortest_path}，速率为{speed}")

    save_graph(SAVE_PATH, r_uovk, NODES)
