class Ship:
    def __init__(self, coord, facing, waypoint=(10, 1)):
        self.coord = coord
        self.facing = facing
        self.waypoint = waypoint

    basis = {"W": (-1, 0), "E": (1, 0), "S": (0, -1), "N": (0, 1)}
    clock_code = {"E": 0, "N": 1, "W": 2, "S": 3}
    hand_code = {"L": 1, "R": -1}

    @staticmethod
    def _add(tup1, tup2):
        return tuple(map(sum, zip(tup1, tup2)))

    @staticmethod
    def _mult(scal, tup):
        return tuple(scal * x for x in tup)

    @staticmethod
    def _clock_rot_cc(tup, quad_cc):  # not proud of this
        def _clock_rot_1_quad_left(tup):
            return -tup[1], tup[0]

        for i in range(quad_cc):
            tup = _clock_rot_1_quad_left(tup)
        return tup

    def p1_step(self, instruction):
        direction, mag = instruction

        if direction in ["W", "E", "S", "N"]:
            add_vec = self._mult(mag, self.basis[direction])
            self.coord = self._add(self.coord, add_vec)
        elif direction == "F":
            add_vec = self._mult(mag, self.basis[self.facing])
            self.coord = self._add(self.coord, add_vec)
        elif direction in ["L", "R"]:
            mag = mag / 90
            new_dir_code = (
                self.clock_code[self.facing] + mag * self.hand_code[direction]
            ) % 4
            self.facing = [k for k, v in self.clock_code.items() if v == new_dir_code][0]
        else:
            raise KeyError(f"instruction: {instruction} not anticipated")

    def p2_step(self, instruction):
        direction, mag = instruction
        if direction in ["W", "E", "S", "N"]:
            add_vec = self._mult(mag, self.basis[direction])
            self.waypoint = self._add(self.waypoint, add_vec)
        elif direction == "F":
            add_vec = self._mult(mag, self.waypoint)
            self.coord = self._add(self.coord, add_vec)
        elif direction in ["L", "R"]:
            mag = int(mag / 90)
            rotate_quad = (mag * self.hand_code[direction]) % 4
            self.waypoint = self._clock_rot_cc(self.waypoint, rotate_quad)
        else:
            raise KeyError(f"instruction: {instruction} not anticipated")


def parse(in_file):
    return [(x[0], int(x[1:])) for x in in_file.readlines()]


def p1(ship, instructions):
    for instr in instructions:
        ship.p1_step(instr)
    return sum(abs(x) for x in ship.coord)


def p2(ship, instructions):
    for instr in instructions:
        ship.p2_step(instr)
    return sum(abs(x) for x in ship.coord)


if __name__ == "__main__":
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        instructions = parse(my_file)

    ship = Ship((0, 0), "E")
    print(f"P1 Answer: {p1(ship, instructions)}")

    ship = Ship((0, 0), "E", waypoint=(10, 1))
    print(f"P2 Answer: {p2(ship, instructions)}")
