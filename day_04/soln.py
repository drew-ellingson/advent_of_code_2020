import re


def parse(in_file):
    # return list of dicts
    raw = in_file.read()
    intm = raw.split("\n\n")  # new record indicator
    intm = [
        x.replace("\n", " ").split(" ") for x in intm
    ]  # delimiter normalization
    clean = [{x.split(":")[0]: x.split(":")[1] for x in y} for y in intm]
    return clean


def is_complete(ppt, valid_keys):
    return set(valid_keys).issubset(set(ppt.keys()))


def is_valid(ppt):
    hgt_re = re.compile("[0-9]{1,}(in|cm)")  # number followed by in or cm
    hcl_re = re.compile("^#([0-9a-f]{6})$")  # '# followed by exactly 6 0-9a-f'
    pid_re = re.compile("^([0-9]{9})$")  # exactly 9 digit number including leading 0s

    def hgt_valid(hgt):
        if not hgt_re.match(hgt):
            return False
        metric = hgt[-2:]
        val = int(hgt[:-2])
        if metric == "in":
            return val >= 59 and val <= 76
        else:
            return val >= 150 and val <= 193

    return all(
        [
            (int(ppt["byr"]) >= 1920 and int(ppt["byr"]) <= 2002),
            (int(ppt["iyr"]) >= 2010 and int(ppt["iyr"]) <= 2020),
            (int(ppt["eyr"]) >= 2020 and int(ppt["eyr"]) <= 2030),
            hgt_valid(ppt["hgt"]),
            hcl_re.match(ppt["hcl"]),
            ppt["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
            pid_re.match(ppt["pid"]),
        ]
    )


def p1(ppts, valid_keys):
    good_ppts = list(filter(lambda x: is_complete(x, valid_keys), ppts))
    return len(good_ppts)


def p2(ppts, valid_keys):
    initial_sweep = list(filter(lambda x: is_complete(x, valid_keys), ppts))
    valid_ppts = list(filter(is_valid, initial_sweep))
    return len(valid_ppts)


if __name__ == "__main__":
    with open("input.txt") as my_file:
        ppts = parse(my_file)
    valid_keys = ["ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"]

    print(f"P1 Answer: {p1(ppts, valid_keys)}")
    print(f"P2 Answer: {p2(ppts, valid_keys)}")
