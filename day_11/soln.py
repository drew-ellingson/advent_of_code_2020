from itertools import product


def parse(in_file):
    """ output dict of {(x,y): status} """
    lines = [x.strip() for x in in_file.readlines()]
    return {(x, y): line[y] for (x, line) in enumerate(lines) for y in range(len(line))}


def get_adjacents(grid, coord):  # improve by prestoring coords?\
    """ return # of adjacent filled seats given a coordinate """
    possible_incs = [-1, 0, 1]
    directions = list(product(possible_incs, possible_incs))
    directions.remove((0, 0))
    adjacent_coords = [tuple(map(sum, zip(coord, delta))) for delta in directions]

    def adj_val(grid, coord):
        try:
            return grid[coord] == "#"
        except KeyError:
            return False

    return sum(adj_val(grid, coord) for coord in adjacent_coords)


def get_line_of_sight_adjacents(grid, coord):
    """ return # of filled seats within line of site given a coordinate"""
    possible_incs = [-1, 0, 1]
    directions = list(product(possible_incs, possible_incs))
    directions.remove((0, 0))
    adjacents = []
    for vec in directions:
        output = coord
        while True:
            output = tuple(map(sum, zip(output, vec)))
            try:
                seat_val = grid[output]
                if seat_val in ("L", "#"):
                    adjacents.append(seat_val)
                    break
            except KeyError:
                break

    return sum(val == "#" for val in adjacents)


def step(grid, adj_func, max_adj):
    """build new_grid from previous according adjacency rules
    adj_func - func(grid, coord) giving 'adjacent' seats filled
    max_adj - the maximum number of adjacent seats someone is willing to abide
    """
    new_grid = {}
    for x, y in grid.keys():
        if grid[(x, y)] == ".":
            new_grid[(x, y)] = "."
        adjacent_occ = adj_func(grid, (x, y))

        if grid[(x, y)] == "L" and adjacent_occ == 0:
            new_grid[(x, y)] = "#"
        elif grid[(x, y)] == "#" and adjacent_occ >= max_adj:
            new_grid[(x, y)] = "L"
        else:
            new_grid[(x, y)] = grid[(x, y)]
    return new_grid


def stabilize(grid, adj_func, max_adj):
    i = 0
    while True:
        print(f"iteration {i}")
        i += 1
        new_grid = step(grid, adj_func, max_adj)
        if new_grid == grid:
            return list(grid.values()).count("#")
        grid = new_grid


if __name__ == "__main__":
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        grid = parse(my_file)

    print(f"P1 Answer: {stabilize(grid, get_adjacents, 4)}")
    print(f"P2 Answer: {stabilize(grid, get_line_of_sight_adjacents, 5)}")
