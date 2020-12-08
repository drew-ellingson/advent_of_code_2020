def parse(in_file):
    instr = [tuple(x.strip().split()) for x in in_file.readlines()]
    instr = list(map(lambda x: (x[0], int(x[1])), instr))
    return instr


def step(instr, indx, acc, past_indx):
    if indx == len(instr):
        raise IndexError(f"P2 Answer: {acc}")
    curr_instr = instr[indx]
    past_indx.append(indx)
    if curr_instr[0] == "nop":
        indx += 1
    elif curr_instr[0] == "acc":
        indx += 1
        acc += curr_instr[1]
    elif curr_instr[0] == "jmp":
        indx += curr_instr[1]
    else:
        raise ValueError(f"{curr_instr[0]} is not a valid operation code")
    return indx, acc, past_indx


def p1(instr):
    acc, indx, past_indx, done = 0, 0, [], False
    while not done:
        indx, acc, past_indx = step(instr, indx, acc, past_indx)
        done = indx in past_indx
    return acc


def gen_mod_set(instr):
    # output a list of instruction sets with one jmp or nop switched per list
    output_instr = []
    for i, line in enumerate(instr):
        if line[0] == "nop":
            new_instr = ("jmp", line[1])
        elif line[0] == "jmp":
            new_instr = ("nop", line[1])
        else:
            continue
        new_instr_set = [
            new_instr if j == i else curr for (j, curr) in enumerate(instr)
        ]
        output_instr.append(new_instr_set)
    return output_instr


def p2(instr):
    for instr_set in gen_mod_set(instr):
        p1(instr_set)
    # answer output is raised in an IndexError in step...


if __name__ == "__main__":
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        instr = parse(my_file)

    print(f"P1 Answer: {p1(instr)}")
    print(f"P2 Answer: {p2(instr)}")
