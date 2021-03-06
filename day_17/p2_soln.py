from itertools import product


class Node:
    def __init__(self, coord, initial_state):
        self.coord = coord
        self.state = initial_state
        self.adjacents = self.get_adjacents()

    @staticmethod
    def _add(tup1, tup2):
        return tuple(map(sum, zip(tup1, tup2)))

    def get_adjacents(self):
        basic = (1, 0, -1)
        deltas = list(product(basic, basic, basic, basic))
        deltas.remove((0, 0, 0, 0))
        adjs = list(map(lambda x: self._add(self.coord, x), deltas))
        return adjs


def parse(in_file):
    lines = [line.strip() for line in in_file.readlines()]
    grid = [
        Node((i, j, 0, 0), line[j])
        for i, line in enumerate(lines)
        for j in range(len(line))
    ]
    return grid


def node_step(grid, cntr_coord):
    try:
        cntr_node = [node for node in grid if node.coord == cntr_coord][0]
    except IndexError:  # handle boundaries with new inactive node
        cntr_node = Node(cntr_coord, ".")

    active_adj_nodes = [
        node for node in grid if node.coord in cntr_node.adjacents and node.state == "#"
    ]

    if cntr_node.state == "#":
        if len(active_adj_nodes) in [2, 3]:
            new_state = "#"
        else:
            new_state = "."
    elif cntr_node.state == "." and len(active_adj_nodes) == 3:
        new_state = "#"
    else:
        new_state = "."

    return Node(cntr_node.coord, new_state)


def grid_step(grid):
    coords_dupe = [coord for node in grid for coord in node.adjacents]
    coords = list(set(coords_dupe))  # really inefficient
    new_grid = [node_step(grid, coord) for coord in coords]
    return new_grid


def p2(grid):
    for i in range(6):  # initial grid doesnt count as a cycle
        print(f"working on cycle {i}")
        grid = grid_step(grid)

    return len([node for node in grid if node.state == "#"])


if __name__ == "__main__":
    # with open("input_test_1.txt") as my_file:
    with open("input.txt") as my_file:
        grid = parse(my_file)

    print(f"P1 Answer: {p2(grid)}")
