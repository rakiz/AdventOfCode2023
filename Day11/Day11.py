import time
from itertools import combinations

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_data(filename):
    with open(filename, "r") as file:
        # get all the coord of the '#'
        g = [(num_col, num_lig) for num_lig, row in enumerate(file) for num_col, char in enumerate(row) if char == '#']
        return g


def execute(grid, exp):
    print("Day 11 - Start")
    t0 = time.perf_counter()

    (xs, ys) = zip(*grid)  # get list of X and list of Y
    empty_xs = [i for i in range(max(xs)) if i not in xs]  # find holes in columns
    empty_ys = [i for i in range(max(ys)) if i not in ys]  # find holes in lines
    possible_distances = list(combinations(grid, 2))  # prepare all possible couples of stars

    result = 0
    for (s1x, s1y), (s2x, s2y) in possible_distances:
        dist = abs(s2x - s1x) + abs(s2y - s1y)  # calculate distances as if evrything was normal
        # find the number of expandable column-galaxies
        nb_x_holes = len(list(filter(lambda x: min(s1x, s2x) <= x <= max(s1x, s2x), empty_xs)))
        # find the number of expandable line-galaxies
        nb_y_holes = len(list(filter(lambda y: min(s1y, s2y) <= y <= max(s1y, s2y), empty_ys)))
        # result is the distance + the expansion of holes
        result += dist + (exp - 1) * (nb_x_holes + nb_y_holes)

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")

    return result


if __name__ == '__main__':
    assert execute(load_data(TEST_FILE), 2) == 374
    assert execute(load_data(INPUT_FILE), 2) == 9795148

    assert execute(load_data(TEST_FILE), 10) == 1030
    assert execute(load_data(TEST_FILE), 100) == 8410
    assert execute(load_data(INPUT_FILE), 1000000) == 650672493820
