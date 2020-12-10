from collections import Counter
from itertools import chain, combinations
from datetime import datetime
import math


def parse(in_file):
    return [int(x) for x in in_file.readlines()]


def prep(jolts):
    """return jolts with wall and max adapter added
    also return a diffs list between sequential adapters
    """
    jolts.append(0)  # add wall
    jolts.append(max(jolts) + 3)  # add max rating
    jolts = sorted(jolts)
    jolt_diffs = [i - j for i, j in zip(jolts[1:], jolts[:-1])]  # sequential diffs
    return jolts, jolt_diffs


def p1(jolt_diffs):
    jolt_diff_hist = Counter(jolt_diffs)
    return jolt_diff_hist[1] * jolt_diff_hist[3]


def gen_sublist(jolt_diffs, index_list):  # thanks mcmanus
    """ return slices from jolt_diffs according to sequential values in index_list
    goal is to return slices between occurrences of '3'
    eg. jolt_diffs = [1,2,3,3,1,1,1,1,3,3,3]
        index_list = [2,3,8,9,10]
    returns: [1,2] and then [1,1,1,1]
    """
    var_list = jolt_diffs[0 : index_list[0]]  # return list until first occurrence of 3
    if len(var_list) >= 2:
        yield var_list
    for i in range(len(index_list) - 1):
        var_list = jolt_diffs[index_list[i] + 1 : index_list[i + 1]]
        if len(var_list) < 2:  # no variations to gain by removing anything in 1 lists
            continue
        yield var_list


def running_sum(sublist):
    """ return list of running sum of len 3 of list """
    return [sum(sublist[max(i-2,0) : i + 1]) for i in range(len(sublist))]


def is_valid(replace_sublist, sublist):
    """ checks whether a diff list is valid when some indices are replaced with 0
    (replace_sublist). This simulates removing the specified adapter from the chain
    eg. if diff seq [1,1,1,1,1] has some elements replaced to [1,0,1,0,1],
        do we still follow adapter rules?
    """
    sublist_cum = running_sum(sublist)
    replace_sublist_cum = running_sum(replace_sublist)
    if replace_sublist[-1] != sublist[-1]:
        return False # last char has to be the same leading into a 3
    return not any(
        sublist_cum[i] - replace_sublist_cum[i] > 2 for i in range(len(sublist))
    )


def replace_index_subset(sublist, index_set):
    """ replace sublist values at indices in index set with 0 """
    return [0 if i in index_set else sublist[i] for i in range(len(sublist))]


def count_sublist_vars(sublist):  # some brute force
    """ generate all possible omissions for the sublist. test each one to see if
    it is valid with the indices removed
    """
    sub_len = len(sublist)
    sub_indices = range(sub_len)

    # generate all combinations of len <= sub_len
    all_index_subsets = chain(
        *map(lambda x: combinations(sub_indices, x), range(0, sub_len + 1))
    )
    all_index_subsets = [list(x) for x in all_index_subsets]

    replacements = [
        replace_index_subset(sublist, index_subset)
        for index_subset in all_index_subsets
    ]
    valids = [
        is_valid(replacement, sublist) for replacement in replacements
    ]
    return sum(valids)


def p2(jolt_diffs):
    fixed_indices = [
        i for i in range(len(jolt_diffs)) if jolt_diffs[i] == 3
    ]  # can't remove a 3 diff without breaking the rules
    variations = [
        count_sublist_vars(sublist)
        for sublist in gen_sublist(jolt_diffs, fixed_indices)
    ]
    return math.prod(variations)


if __name__ == "__main__":
    test_list_1 = [1, 1, 1, 1, 1]
    test_list_2 = [1, 0, 1, 0, 1]
    test_list_3 = [1, 0, 0, 0, 1]
    test_list_4 = [1, 1, 1, 1, 0]
    test_list_5 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    test_list_6 = [1, 0, 1 ,0 ,1, 0, 1, 0, 1, 0, 1]

    assert running_sum(test_list_1) == [1, 2, 3, 3, 3]
    assert running_sum(test_list_2) == [1, 1, 2, 1, 2]

    assert is_valid(test_list_2, test_list_1)
    assert not is_valid(test_list_3, test_list_1)
    assert not is_valid(test_list_4, test_list_1)
    assert is_valid(test_list_6, test_list_5)

    assert replace_index_subset(test_list_1, [1, 2, 3]) == test_list_3
    
    start_time = datetime.now()
    
    # with open('input_test_1.txt') as my_file:
    # with open('input_test_2.txt') as my_file:
    with open("input.txt") as my_file:
        jolts = parse(my_file)

    jolts, jolt_diffs = prep(jolts)

    print(f"P1 Answer: {p1(jolt_diffs)}")
    print(f"P2 Answer: {p2(jolt_diffs)}")
    print(f" total time: {datetime.now() - start_time}")
