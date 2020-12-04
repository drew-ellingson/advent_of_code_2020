from collections import Counter


def parse(in_file):
    raw_pass = in_file.readlines()
    raw_pass = [x.replace("-", " ").replace(":", "") for x in raw_pass]
    raw_pass = [x.split(" ") for x in raw_pass]
    clean_pass = [
        {
            "pass": one_pass[3],
            "letter": one_pass[2],
            "min_count": int(one_pass[0]),
            "max_count": int(one_pass[1]),
        }
        for one_pass in raw_pass
    ]
    return clean_pass


def is_valid_v1(password):
    hist = Counter(password["pass"])
    return (
        hist[password["letter"]] >= password["min_count"]
        and hist[password["letter"]] <= password["max_count"]
    )


def is_valid_v2(password):
    first_cand = password["pass"][password["min_count"] - 1]  # 1-index
    second_cand = password["pass"][password["max_count"] - 1]

    # xor
    return (first_cand == password["letter"]) != (second_cand == password["letter"])


def p1(passwords):
    valid_pass = list(filter(is_valid_v1, passwords))
    return len(valid_pass)


def p2(passwords):
    valid_pass = list(filter(is_valid_v2, passwords))
    return len(valid_pass)


if __name__ == "__main__":
    with open("input.txt") as my_file:
        passwords = parse(my_file)

    print(f"P1 Answer: {p1(passwords)}")
    print(f"P2 Answer: {p2(passwords)}")
