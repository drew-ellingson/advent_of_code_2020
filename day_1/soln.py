def p1(nums):
    # ignoring any 1010s
    x, y = [(x, y) for x in nums for y in nums if x + y == 2020][0]
    return x * y


def p2(nums):
    x, y, z = [
        (x, y, z) for x in nums for y in nums for z in nums if x + y + z == 2020
    ][0]
    return x * y * z


if __name__ == "__main__":
    with open("input.txt") as my_file:
        nums = [int(x.strip()) for x in my_file.readlines()]
    print(f'P1 Answer: {p1(nums)}')
    print(f'P2 Answer: {p2(nums)}')
