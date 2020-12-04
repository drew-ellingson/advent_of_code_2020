import math


def parse(in_file):
    # output list of list of chars
    tree_lines = in_file.readlines()
    tree_lines = [[y for y in x.strip()] for x in tree_lines]
    return tree_lines


def step(tree_lines, start_y, start_x, down_del, right_del):
    # returns whether there is a collison after moving the specified step
    net_down_del = start_y + down_del
    net_right_del = (start_x + right_del) % len(tree_lines[0])
    end_y = start_y + net_down_del
    end_x = start_x + net_right_del
    return tree_lines[end_y][end_x] == "#"


def p1(tree_lines, down_del, right_del):
    # counts collisions on a given slope
    step_count = int(len(tree_lines) / down_del)  # assuming divisible
    steps = [
        step(tree_lines, 0, 0, i * down_del, i * right_del)
        for i in range(1, step_count)
    ]
    return sum(steps)


def p2(tree_lines, slopes):
    # counts collisions on a list of slopes, takes product
    steps = {(i, j): p1(tree_lines, i, j) for (i, j) in slopes}
    return math.prod(steps.values())


if __name__ == "__main__":
    # with open("input_test_1.txt") as my_file:
    with open("input.txt") as my_file:
        tree_lines = parse(my_file)

    slope = (1, 3)
    print(f"P1 Answer: {p1(tree_lines, *slope)}")

    slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
    print(f"P2 Answer: {p2(tree_lines, slopes)}")
