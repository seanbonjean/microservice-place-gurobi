import random


def link_value_generator():
    if random.random() < 0.2:
        return 0
    else:
        return random.randint(1, 9)


def generate_graph(path: str, edgenode_count: int):
    with open(path, 'w') as f:
        for i in range(edgenode_count):
            line = ''
            for j in range(edgenode_count):
                if i < j:
                    line += str(link_value_generator()) + ' '
                else:
                    line += '* '
            f.write(line.strip() + '\n')


if __name__ == '__main__':
    NODES = 10
    SAVE_PATH = 'graph/data/sparse2.txt'
    generate_graph(SAVE_PATH, NODES)
