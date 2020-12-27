from collections import Counter
from functools import reduce
from itertools import chain

UNITS = {
    "e": (1, 0),
    "w": (-1, 0),
    "ne": (0.5, 1),
    "nw": (-0.5, 1),
    "se": (0.5, -1),
    "sw": (-0.5, -1),
}


def _add(tup1, tup2):
    return tuple(map(sum, zip(tup1, tup2)))


class Tile:
    def __init__(self, coord):
        self.coord = coord
        self.adj_coords = self.get_adj_coords()

    def get_adj_coords(self):
        return set([_add(self.coord, unit) for unit in UNITS.values()])


class Grid:
    def __init__(self, black_tiles):
        self.black_tiles = black_tiles

    def one_step(self):
        black_coords = set([x.coord for x in self.black_tiles])
        black_stay = filter(
            lambda x: len(x.adj_coords.intersection(black_coords)) in [1, 2],
            self.black_tiles,
        )

        adj_coords = chain(*[x.adj_coords for x in self.black_tiles])
        adj_white_coords = filter(lambda x: x not in black_coords, adj_coords)
        white_flip = [k for k, v in Counter(adj_white_coords).items() if v == 2]
        white_flip_tiles = [Tile(x) for x in white_flip]

        self.black_tiles = list(black_stay) + white_flip_tiles

    def many_step(self, iters):
        for i in range(iters):
            self.one_step()


def parse_line(tile_line):
    tile_directs = []
    while len(tile_line) > 0:
        if tile_line[:2] in ["se", "ne", "nw", "sw"]:
            tile_directs.append(tile_line[:2])
            tile_line = tile_line[2:]
        else:
            tile_directs.append(tile_line[0])
            tile_line = tile_line[1:]
    return tile_directs


def parse(in_file):
    tiles_raw = [x.strip() for x in in_file.readlines()]
    return list(map(parse_line, tiles_raw))


def get_coord(td):
    coord_adds = [UNITS[x] for x in td]
    return reduce(lambda a, b: _add(a, b), coord_adds)


def get_init_black_tiles(tds):
    canon_tds = list(map(get_coord, tds))
    occ_canon_tds = Counter(canon_tds)
    black_tiles = [Tile(k) for k, v in occ_canon_tds.items() if v % 2 == 1]
    return black_tiles


if __name__ == "__main__":
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        tile_directs = parse(my_file)

    black_tiles = get_init_black_tiles(tile_directs)
    print(f"P1 Answer: {len(black_tiles)}")

    grid = Grid(black_tiles)
    grid.many_step(100)

    print(f"P2 Answer: {len(grid.black_tiles)}")
