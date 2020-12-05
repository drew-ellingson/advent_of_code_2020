import re


def parse(in_file):
    # return list of (row, seat) tuples
    raw = [x.strip() for x in in_file.readlines()]
    seat_address = [(x[:7], x[7:]) for x in raw]
    return seat_address

def addr_conv(address, keys):
    # convert a BFBFB or RLRLRL to int using lookup dict 'keys'
    try:
        return sum([2**(len(address)-i - 1) * keys[address[i]] for i in range(len(address))])
    except KeyError:
        print(f'Issue with dict key for {address[i]} at pos {i} in address {address}')

def get_seat_id(row, col):
    return 8 * row + col 

def p1(seats, bf_lkp, lr_lkp):
    return max([get_seat_id(addr_conv(row, bf_lkp), addr_conv(col, lr_lkp)) for (row, col) in seats])


def p2(seats, bf_lkp, lr_lkp):
    seat_ids = [get_seat_id(addr_conv(row, bf_lkp), addr_conv(col, lr_lkp)) for (row, col) in seats]
    seat_ids = sorted(seat_ids)
    missing_seat = min([x for x in seat_ids if x+1 not in seat_ids]) + 1
    return missing_seat


if __name__ == "__main__":
    with open("input.txt") as my_file:
        seats = parse(my_file)
    
    bf_lkp = {'B': 1, 'F': 0}
    lr_lkp = {'R': 1, 'L': 0}

    # few test cases
    assert(addr_conv('BFFFBBF', bf_lkp) == 70)
    assert(addr_conv('RRR', lr_lkp) == 7)

    print(f"P1 Answer: {p1(seats, bf_lkp, lr_lkp)}")
    print(f"P2 Answer: {p2(seats, bf_lkp, lr_lkp)}")
