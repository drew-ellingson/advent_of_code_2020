def parse(in_file):
    groups = in_file.read().split('\n\n')
    return groups


def p1(groups):
    group_yes = [group.replace('\n','') for group in groups] # read in all answers together
    group_yes_dedup = [set(group) for group in group_yes]
    return sum([len(yes) for yes in group_yes_dedup])


def p2(groups):
    groups = [group.split('\n') for group in groups] # answers per group member
    cands = range(ord('a'), ord('z') + 1)
    all_yes = [all(chr(val) in person for person in group) for group in groups for val in cands]
    return sum(all_yes)

if __name__ == "__main__":
    with open("input.txt") as my_file:
        groups = parse(my_file)

    print(f"P1 Answer: {p1(groups)}")
    print(f"P2 Answer: {p2(groups)}")
