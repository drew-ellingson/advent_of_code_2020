def parse(in_file):
    # return dict of {container: {contained: count}}
    def parse_line(line):
        line = line.replace(".", "").replace(" bags", "").replace(" bag", "")
        container, contained = line.split(" contain ")
        contained = [x.strip() for x in contained.split(",")]
        try:
            contained = {
                x[x.index(" ") + 1 :]: int(x[: x.index(" ")]) for x in contained
            }
        except ValueError:  # catch int('no') errors for leaves on the tree
            contained = {}
        return container, contained

    out = {k: v for k, v in map(parse_line, in_file.readlines())}
    return out


def up_one(rules, target_bag):
    contain_bags = dict(filter(lambda x: target_bag in x[1].keys(), rules.items()))
    return contain_bags


def p1(rules, target_bag):
    containers = {target_bag: rules[target_bag]}
    done = False
    while not done:
        new_containers = [up_one(rules, bag) for bag in containers]
        new_containers = {k: v for bag in new_containers for k, v in bag.items()}
        new_containers = {**containers, **new_containers}

        if len(new_containers.keys()) == len(containers.keys()):
            done = True
        else:
            containers = {**containers, **new_containers}
    return len(containers.keys()) - 1  # the target bag itself isn't included


def p2(rules, target_bag):  # this is wrong but I don't know why. works on both testcases
    weights = {}
    weights[target_bag] = 1

    def assign_weights(rules, curr_bag):
        for bag, count in rules[curr_bag].items():  # contained bags dict
            try:
                weights[bag] += weights[curr_bag] * count
            except KeyError:  # new entry
                weights[bag] = weights[curr_bag] * count
            assign_weights(rules, bag)
        return weights

    weights = assign_weights(rules, target_bag)

    return sum(weights.values()) - weights[target_bag] # don't include target_bag


def p2_v2(rules, target_bag):
    def bags_contained(bag, rules):
        if rules[bag] == {}:
            return 1
        else:
            return 1 + sum(
                count * bags_contained(inside_bag, rules)
                for inside_bag, count in rules[bag].items()
            )  # include bag itself

    return bags_contained(target_bag, rules) - 1  # don't include target bag


if __name__ == "__main__":
    # with open('input_test_1.txt') as my_file:
    # with open('input_test_2.txt') as my_file:
    with open("input.txt") as my_file:
        rules = parse(my_file)
    target_bag = "shiny gold"

    print(f"P1 Answer: {p1(rules, target_bag)}")
    print(f"P2 Answer: {p2(rules, target_bag)}")
    print(f"P2_v2 Answer: {p2_v2(rules, target_bag)}")
