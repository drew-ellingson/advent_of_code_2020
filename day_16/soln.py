from collections import defaultdict
from math import prod


def parse_range(line):
    key, val = line.split(": ")
    val = [list(map(int, rng.split("-"))) for rng in val.split(" or ")]
    return key, val


def parse_ticket(line):
    return list(map(int, line.split(",")))


def parse(in_file):
    """return {field: [[min1,max1], [min2,max2]}, [ticket], [[tickets]] """
    comps = my_file.read().split("\n\n")

    ranges = comps[0].split("\n")
    ranges = {k: v for k, v in map(parse_range, ranges)}

    my_ticket = comps[1].split("\n")[1:]  # remove 'your ticket' row
    my_ticket = parse_ticket(my_ticket[0])

    nearby_tickets = comps[2].split("\n")[1:]  # remove 'nearby ticket' row
    nearby_tickets = [parse_ticket(ticket) for ticket in nearby_tickets]

    return ranges, my_ticket, nearby_tickets


def get_min_max(tickets):
    """return smallest and largest val from a list of tickets"""
    flat_val = [i for ticket in tickets for i in ticket]
    return min(flat_val), max(flat_val)


def get_invalid_nums(ranges, min_val, max_val):
    """ build a list of numbers not in any range within the (min_val, max_val)"""
    range_only = [rng for pair_of_rng in ranges.values() for rng in pair_of_rng]

    invalids = [
        i
        for i in range(min_val, max_val + 1)
        if not any(rng[0] <= i <= rng[1] for rng in range_only)
    ]
    return invalids


def p1(ranges, nearby_tickets):
    min_val, max_val = get_min_max(nearby_tickets)
    invalids = get_invalid_nums(ranges, min_val, max_val)
    return sum(sum(i for i in ticket if i in invalids) for ticket in nearby_tickets)


def p2(ranges, my_ticket, nearby_tickets):
    min_val, max_val = get_min_max(nearby_tickets)
    invalids = get_invalid_nums(ranges, min_val, max_val)
    valid_tickets = [
        ticket for ticket in nearby_tickets if not any(i in invalids for i in ticket)
    ]

    def find_val_field_pos(ranges, valid_tickets):
        """for each field, return the positions it can occupy valid for all valid tickets
        eg. 'row': [0,1,2], 'class': [1,2], 'seat': [2]"""
        fields = defaultdict(list)
        for i in range(len(valid_tickets[0])):
            for j, [range1, range2] in ranges.items():
                ticket_rgn_vals = [ticket[i] for ticket in valid_tickets]
                if all(
                    range1[0] <= val <= range1[1] or range2[0] <= val <= range2[1]
                    for val in ticket_rgn_vals
                ):
                    fields[j].append(i)
        return fields

    valid_field_pos = find_val_field_pos(ranges, valid_tickets)

    field_assign = {}

    def assign_lowhanging_fruit(valid_field_pos, field_assign):
        """this reduces the problem if there are any fields that can only fit in one 
        position - not guaranteed if there is more complex logic that needs to happen"""
        for field, val_pos in valid_field_pos.items():
            if len(val_pos) == 1:
                field_assign[field] = val_pos[0]
        for key in field_assign.keys():
            try:
                valid_field_pos.pop(key)
            except KeyError:
                pass
        assigned = field_assign.values()
        for field in valid_field_pos.keys():
            valid_field_pos[field] = [
                i for i in valid_field_pos[field] if i not in assigned
            ]
        return valid_field_pos, field_assign

    while True:
        if len(valid_field_pos.keys()) == 0:
            break
        valid_field_pos, field_assign = assign_lowhanging_fruit(
            valid_field_pos, field_assign
        )

    departure_fields = [v for k, v in field_assign.items() if k.startswith("departure")]
    return prod(my_ticket[i] for i in departure_fields)


if __name__ == "__main__":
    # with open('input_test_2.txt') as my_file:
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        ranges, my_ticket, nearby_tickets = parse(my_file)

    print(f"P1 Answer: {p1(ranges, nearby_tickets)}")
    print(f"P2 Answer: {p2(ranges, my_ticket, nearby_tickets)}")
