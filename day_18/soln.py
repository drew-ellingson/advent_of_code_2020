import pyparsing as pp
from math import prod


def get_exprs(in_file):
    """read input into parsed list of lists representing expressions """
    lines = [line.strip() for line in in_file.readlines()]
    return list(map(parse_expr, lines))


def parse_expr(line):
    """convert string number sentence into nested list expressions 
        eg. "1+(2*3)" --> ['1', '+', ['2', '*', '3']]
    """
    line = "(" + line.replace(" ", "") + ")"
    eq_content = pp.Word(pp.nums) | "+" | "*"
    nest = pp.nestedExpr("(", ")", content=eq_content)
    nested_eq = nest.parseString(line)
    return nested_eq.asList()


def new_math_eval(parsed_expr):
    """recursively handle expression calculation for p1"""
    curr_val, curr_op = 0, "+"
    for elem in parsed_expr:
        if type(elem) == list:
            elem = new_math_eval(elem)

        if elem not in ["+", "*"]:
            if curr_op == "+":
                curr_val += int(elem)
            elif curr_op == "*":
                curr_val *= int(elem)
            else:
                raise ValueError(f"operation {curr_op} not recognized")
        else:
            curr_op = elem
    return curr_val


def adv_math_eval(parsed_expr):
    """recursively remove parens using adv_math_simple for p2 """
    for i, elem in enumerate(parsed_expr):
        if type(elem) == list and all(not type(item) == list for item in elem):
            parsed_expr[i] = adv_math_simple(elem)
        else:
            if type(elem) == list:
                parsed_expr[i] = adv_math_eval(elem)
    return adv_math_simple(parsed_expr)


def adv_math_simple(parsed_expr):
    """recusively handle simple expressions w/o parens according to p2 rules"""
    try:
        add_indx = parsed_expr.index("+")
    except ValueError:
        return str(prod(int(a) for a in parsed_expr if a != "*"))

    sub_calc = parsed_expr[add_indx - 1 : add_indx + 2]
    new_val = int(sub_calc[0]) + int(sub_calc[2])

    reduced = parsed_expr[: add_indx - 1] + [str(new_val)] + parsed_expr[add_indx + 2 :]
    return str(adv_math_simple(reduced))


def p1(probs):
    return sum(new_math_eval(prob) for prob in probs)


def p2(probs):
    return sum(int(adv_math_eval(prob)) for prob in probs)


if __name__ == "__main__":
    with open("input.txt") as my_file:
        exprs = get_exprs(my_file)

    print(f"P1 Answer: {p1(exprs)}")
    print(f"P2 Answer: {p2(exprs)}")
