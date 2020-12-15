import math

def parse(in_file):
    lines = in_file.readlines()
    timestamp = int(lines[0].strip())
    raw_buslist = lines[1].split(',')
    
    congruences = [(int(val), int(val) - i) for i,val in enumerate(raw_buslist) if val != 'x']
    buslist = [x[0] for x in congruences]

    return timestamp, buslist, congruences

def p1(avail_ts, buslist):
    ts = {k: math.ceil(avail_ts / k) * k for k in buslist} 
    first_bus, first_ts = min(ts.items(), key=lambda x: x[1])
    return first_bus * (first_ts - avail_ts)

def p2(congruences): # chinese remainder
    curr_sum = 0
    prod = math.prod(item[0] for item in congruences)

    def mult_inv(a, b): # extended euclidean algorithm
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = mult_inv(b% a, a)
        x = y1 - math.floor(b/a) * x1 
        y = x1
        return gcd, x, y


    for ni, ai in congruences:
        p = math.floor(prod / ni)
        curr_sum += ai * mult_inv(p, ni)[1] * p 

    return curr_sum % prod


if __name__ == "__main__":
    # with open('input_test_1.txt') as my_file:
    with open("input.txt") as my_file:
        avail_ts, buslist, congruences = parse(my_file)

    print(f"P1 Answer: {p1(avail_ts, buslist)}")
    print(f"P2 Answer: {p2(congruences)}")