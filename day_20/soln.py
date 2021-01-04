import math 
import random
from collections import Counter 

class Tile():
    def __init__(self, tile_line):
        num, content = tile_line.split(':\n')
        content = content.split('\n')

        self.num = int(num.split(' ')[1])
        self.content = {(x,y): line[x] for y,line in enumerate(content) for x in range(len(line))}
        
        max_x = max(x[0] for x in self.content.keys())
        max_y = max(x[1] for x in self.content.keys())

        if max_x == max_y:
            self.size = max_x + 1
        else:
            raise ValueError(f'non square tile detected {self.num}: {self.content}')

        self.l_edge = self.get_edge('l')
        self.r_edge = self.get_edge('r')
        self.t_edge = self.get_edge('t')
        self.b_edge = self.get_edge('b')

    def get_edge(self, edge):
        """ edge in ['l', 'r', 't', 'b'] 
            return list expr of edge in lexicographic coord order
        """
        full_content = sorted(self.content.items(), key = lambda x: x[0])
        if edge == 'l':
            edge_out = [v for k,v in full_content if k[0] == 0]
        elif edge == 'r':
            edge_out =  [v for k,v in full_content if k[0] == self.size - 1]
        elif edge == 't':
            edge_out =  [v for k,v in full_content if k[1] == 0]
        elif edge == 'b':
            edge_out =  [v for k,v in full_content if k[1] == self.size - 1]
        else:
            raise ValueError(f'unexpected edge designation: {edge}')
        return ''.join(edge_out)
    
    def rotate_cw(self):
        """ rotate a tile 90 degrees clockwise """
        self.content = {(x,y): self.content[(y, self.size - x - 1)] for (x,y) in self.content.keys()}

        temp = self.t_edge
        self.t_edge = ''.join(reversed(self.l_edge))
        self.l_edge = self.b_edge
        self.b_edge = ''.join(reversed(self.r_edge))
        self.r_edge = temp

    def flip(self, orientation):
        """ orientation in ['h', 'v']. flips vertically or horizontally """
        if orientation == 'v':
            self.content = {(x,y): self.content[(x, self.size - y - 1)] for (x,y) in self.content.keys()}
            
            temp = self.t_edge 
            self.t_edge = self.b_edge 
            self.b_edge = temp
        elif orientation == 'h':
            self.content = {(x,y): self.content[(self.size - x - 1, y)] for (x,y) in self.content.keys()}

            temp = self.l_edge
            self.l_edge = self.r_edge 
            self.r_edge = temp    
        else:
            raise ValueError(f'unexpected orientation {orientation}')

    def print_tile(self):
        print(f'Tile Number: {self.num}')
        for y in range(self.size):
            row = [v for k,v in self.content.items() if k[1] == y]
            print(' '.join(row))
        print('\n')
        print(f'top edge {self.t_edge}')
        print(f'right edge {self.r_edge}')
        print(f'bottom edge {self.b_edge}')
        print(f'left edge {self.l_edge}')
        print('\n')

class Grid():
    def __init__(self, tiles):
        if math.isqrt(len(tiles)) ** 2 == len(tiles):
            self.size = int(math.sqrt(len(tiles)))
        else:
            raise ValueError(f'{len(tiles)} tiles doesnt make a perfect square')
        self.tiles = tiles
        self.grid_arr = {}

    @staticmethod
    def _add(tup1, tup2):
        return tuple(map(sum, zip(tup1, tup2)))

    def get_neighbor_coords(self, coord):
        deltas = [(1,0), (-1,0), (0,1), (0, -1)]
        neighbors = list(map(lambda x: self._add(x, coord), deltas))
        neighbors = [(x,y) for (x,y) in neighbors if 0 <= x <= self.size and 0 <= y <= self.size]
        return neighbors 

    def place_tile(self, tile, coord):
        neighbors = self.get_neighbor_coords(coord)
        assigned_neighbors = [x for x in neighbors if x in self.grid_arr.keys()]

    
    def fill_grid(self):
        pass

    def get_edge_tiles(self):
        edges = {}
        for tile in self.tiles:
            for edge in [tile.t_edge, tile.r_edge, tile.b_edge, tile.l_edge]:
                if edge not in edges.keys() and ''.join(reversed(edge)) not in edges.keys():
                    edges[edge] = [tile.num]
                elif edge in edges.keys():
                    edges[edge].append(tile.num)
                elif ''.join(reversed(edge)) in edges.keys():
                    edges[''.join(reversed(edge))].append(tile.num)
        return edges


def parse(in_file):
    return [Tile(entry) for entry in in_file.read().split('\n\n')]
    

def p1(grid):
    shared_edge_counts = grid.get_edge_tiles()
    edge_edges= [(x,y) for (x,y) in shared_edge_counts.items() if len(y) == 1] # hah
    edge_edge_freqs = Counter(x[1][0] for x in edge_edges)
    corners = [x for x,v in edge_edge_freqs.items() if v == 2]
    return math.prod(corners)


def p2():
    pass

if __name__ == "__main__":
    # with open("input_test_1.txt") as my_file:
    with open('input.txt') as my_file:
        tiles = parse(my_file)

    grid = Grid(tiles)
    edge_freqs = grid.get_edge_tiles()


    print(f"P1 Answer: {p1(grid)}")
    print(f"P2 Answer: {p2()}")
