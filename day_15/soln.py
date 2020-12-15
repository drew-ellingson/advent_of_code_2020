def get_num(nums, index):
    while True:
        head, cand = nums[:-1], nums[-1]
        if cand in head:
            new_val = list(reversed(head)).index(cand) + 1
            nums.append(new_val)
        else:
            nums.append(0)
        if len(nums) >= index:
            break
    return nums[index - 1]


from datetime import datetime


def get_num_v2(nums, index):
    starttime = datetime.now()
    most_rec = {val: [indx] for indx, val in enumerate(nums)}
    curr_indx = len(nums)
    cand = nums[-1]
    while True:
        try:
            new_val = curr_indx - most_rec[cand][-2] - 1
        except IndexError:
            new_val = 0

        try:
            most_rec[new_val].append(curr_indx)
        except KeyError:
            most_rec[new_val] = [curr_indx]

        curr_indx += 1
        cand = new_val

        if curr_indx == index:
            break

        if curr_indx % 100000 == 0:  # i am impatient
            print(
                f"completed {curr_indx} out of {index} runs for \
                {round(100 * curr_indx / index,2)}% completion in \
                {datetime.now() - starttime}"
            )

    return [k for k, v in most_rec.items() if index - 1 in v][0]


if __name__ == "__main__":
    # initial_nums = [0,3,6]
    initial_nums = [19, 20, 14, 0, 9, 1]
    print(f"P1 Answer: {get_num(initial_nums, 2020)}")

    # initial_nums = [0,3,6]
    initial_nums = [19, 20, 14, 0, 9, 1]
    print(f"P2 Answer: {get_num_v2(initial_nums, 30000000)}")
