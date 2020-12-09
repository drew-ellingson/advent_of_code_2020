def parse(in_file):
    return [int(x) for x in in_file.readlines()]


def is_valid(instr, indx, preamble_len):
    if indx < preamble_len:
        return True
    curr = instr[indx]
    previous = instr[indx - preamble_len : indx]
    sum_pairs = [(x, y) for x in previous for y in previous if x + y == curr and x != y]
    return len(sum_pairs) != 0


def p1(instr, preamble_len):
    instr_valid = list(
        map(lambda x: is_valid(instr, x, preamble_len), range(len(instr)))
    )
    return instr[instr_valid.index(False)]


def p2(instr, preamble_len):
    inv_num = p1(instr, preamble_len)
    done = False
    for i in range(len(instr)):
        if done:
            break
        base_val = instr[i]
        sum_nums = [base_val]
        for j in range(len(instr))[i + 1 :]:  # subsequent numbers in list
            add_val = instr[j]
            sum_nums.append(add_val)
            if sum(sum_nums) == inv_num:
                done = True
                break
            elif sum(sum_nums) > inv_num:
                break
    if not done:
        raise RuntimeError(f"No sublist found adding to invalid num {inv_num}")
    return max(sum_nums) + min(sum_nums)


if __name__ == "__main__":
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        instr = parse(my_file)
    preamble_len = 25

    print(f"P1 Answer: {p1(instr, preamble_len)}")
    print(f"P2 Answer: {p2(instr, preamble_len)}")
