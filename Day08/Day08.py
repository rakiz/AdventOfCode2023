import re
import time
from math import lcm
from functools import reduce

INPUT_FILE = "input.txt"
TEST1_FILE = "test1.txt"
TEST2_FILE = "test2.txt"
TEST3_FILE = "test3.txt"


def load_file(filename):
    with open(filename) as f:
        data = [re.findall(r"\w+", line) for line in f.read().strip().split("\n")]

    pattern = data[0][0]
    routes = {route[0]: (route[1], route[2]) for route in data[2:]}

    return pattern, routes


def apply(pattern, routes, is_part2):
    print(f"Day 08 (part2={is_part2}) - Start")
    t0 = time.time_ns()

    starts = [k for k in routes.keys() if k[-1] == "A"] if is_part2 else ["AAA"]
    print(f"starts:{starts}")

    counts = [0] * len(starts)  # keep a count for each route
    for i, start in enumerate(starts):
        while (start[-1] != "Z" and is_part2) or (start != "ZZZ" and not is_part2):
            for direction in pattern:
                start = routes[start][0 if direction == "L" else 1]  # start => (left, right)
                counts[i] += 1

    result = reduce(lcm, counts)  # And now, just let find the Least Common Multiple

    t1 = time.time_ns()
    print("End ({}ms) - result = {}\n".format((t1 - t0) / 1000000, result))
    return result


if __name__ == '__main__':
    patternT1, routesT1 = load_file(TEST1_FILE)
    patternT2, routesT2 = load_file(TEST2_FILE)
    patternT3, routesT3 = load_file(TEST3_FILE)
    patternI, routesI = load_file(INPUT_FILE)

    assert apply(patternT1, routesT1, False) == 2
    assert apply(patternT2, routesT2, False) == 6
    assert apply(patternI, routesI, False) == 17873

    assert apply(patternT3, routesT3, True) == 6
    assert apply(patternI, routesI, True) == 15746133679061
