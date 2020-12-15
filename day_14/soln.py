from itertools import product


def handle_line(line):
    """ return (op_type, addr, val) triples """
    instr = line.strip().split(" = ")
    if instr[0] == "mask":
        return "mask", None, instr[1]
    else:
        addr = int(instr[0].replace("mem[", "").replace("]", ""))
        return "store", addr, int(instr[1])


def parse(in_file):
    return [handle_line(line) for line in in_file.readlines()]


def get_bin_str(number):
    """ convert decimal repr int to left padded len-36 str repr of binary """
    unpadded_bin = str(bin(number)[2:])
    return unpadded_bin.zfill(36)


def get_dec_num(bin_str):
    """ convert binary string to decimal """
    return int(bin_str, 2)


def find_real_val(num, mask):
    """ what value actually gets stored for a given mask """
    des_str = get_bin_str(num)
    cands = zip(des_str, mask)
    actual_str = "".join(map(lambda x: x[1] if x[1] != "X" else x[0], cands))
    return get_dec_num(actual_str)


def p1(lines):
    register_vals = {}
    for op, addr, val in lines:
        if op == "mask":
            mask = val
        elif op == "store":
            stored_val = find_real_val(val, mask)
            register_vals[addr] = stored_val
        else:
            raise ValueError(f"operation {op} not recognized")
    return sum(register_vals.values())


def flatten(some_tuple):
    """ remove nesting from arbitrary nested tuples into flat tuples """
    for item in some_tuple:
        if isinstance(item, tuple):
            yield from flatten(item)
        else:
            yield item


def get_tgt_addrs(num, mask):
    """ get all target addresses given a number and a mask - includes floating logic """
    des_str = get_bin_str(num)
    cands = zip(des_str, mask)
    actual_str = "".join(
        map(lambda x: x[0] if x[1] == "0" else "1" if x[1] == "1" else "X", cands)
    )

    var_count = actual_str.count("X")
    basis = (0, 1)
    curr_basis = basis
    for i in range(var_count - 1):
        curr_basis = [x for x in product(curr_basis, basis)]

    # eg. (0,1)^3 = [(0,0,0), (0,0,1) ... (1,1,1)]
    curr_basis = [tuple(flatten(item)) for item in curr_basis]

    output_nums = []
    for x in curr_basis:
        cand = actual_str
        for y in x:
            cand = cand.replace("X", str(y), 1)
        output_nums.append(get_dec_num(cand))

    return output_nums


def p2(lines):
    register_vals = {}
    for i, (op, addr, val) in enumerate(lines):
        if op == "mask":
            mask = val
        elif op == "store":
            regs = get_tgt_addrs(addr, mask)
            for reg in regs:
                register_vals[reg] = val
        else:
            raise ValueError(f"operation {op} not recognized")
    return sum(register_vals.values())


if __name__ == "__main__":
    assert get_bin_str(11) == "000000000000000000000000000000001011"
    assert get_bin_str(101) == "000000000000000000000000000001100101"

    assert get_dec_num("000000000000000000000000000000001011") == 11
    assert get_dec_num("000000000000000000000000000001100101") == 101

    assert find_real_val(11, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 73
    assert find_real_val(101, "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X") == 101

    assert tuple(flatten(((0, 0), 0))) == (0, 0, 0)
    assert tuple(flatten((((0, 0), 0), (0, 0), (0, 0)))) == (0, 0, 0, 0, 0, 0, 0)

    assert get_tgt_addrs(42, "000000000000000000000000000000X1001X") == [26, 27, 58, 59]
    assert get_tgt_addrs(26, "00000000000000000000000000000000X0XX") == [
        16,
        17,
        18,
        19,
        24,
        25,
        26,
        27,
    ]

    # with open('input_test_2.txt') as my_file:
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        lines = parse(my_file)

    print(f"P1 Answer: {p1(lines)}")
    print(f"P2 Answer: {p2(lines)}")
