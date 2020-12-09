def parse(in_file):
    return [int(x) for x in in_file.readlines()]


def is_valid(nums, indx, preamble_len):
    if indx < preamble_len:
        return True
    curr = nums[indx]
    previous = nums[indx - preamble_len : indx]
    sum_pairs = [(x, y) for x in previous for y in previous if x + y == curr and x != y]
    return len(sum_pairs) != 0


def p1(nums, preamble_len):
    num_valid = list(
        map(lambda x: is_valid(nums, x, preamble_len), range(len(nums)))
    )
    return nums[num_valid.index(False)]


def p2(nums, preamble_len):
    inv_num = p1(nums, preamble_len)
    done = False
    for i in range(len(nums)):
        if done:
            break
        base_val = nums[i]
        sum_nums = [base_val]
        for j in range(len(nums))[i + 1 :]:  # subsequent numbers in list
            add_val = nums[j]
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
        nums = parse(my_file)
    preamble_len = 25

    print(f"P1 Answer: {p1(nums, preamble_len)}")
    print(f"P2 Answer: {p2(nums, preamble_len)}")
