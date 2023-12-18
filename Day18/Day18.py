import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_data(filename):
    with open(filename, "r") as file:
        return [(a, int(b), c.strip('()')) for a, b, c in (line.split() for line in file)]


fix_direction = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}


def fix_data(data):
    return [[fix_direction[color[-1]], int(color[1:-1], 16)] for _, _, color in data]


apply_direction = {'U': (0, -1), 'L': (-1, 0), 'D': (0, 1), 'R': (1, 0)}


def execute(data, is_part1):
    print(f"Day 18 part {'1' if is_part1 else '2'} - Start")
    t0 = time.perf_counter()

    if not is_part1:
        data = [[fix_direction[color[-1]], int(color[1:-1], 16)] for _, _, color in data]

    vertices = [(0, 0)]  # we always start in the top left corner of the grid
    for direction, distance, *_ in data:
        move = apply_direction[direction]  # we map the direction and the vector
        # we start from last one in the list
        next_vertex = (vertices[-1][0] + move[0] * distance, vertices[-1][1] + move[1] * distance)
        vertices.append(next_vertex)

    # https://www.101computing.net/the-shoelace-algorithm/
    # sum1, sum2 = 0, 0
    # nb_vertices = len(vertices)
    # for i in range(nb_vertices - 2):  # check if it's -2 ?
    #     sum1 += vertices[i][0] * vertices[i + 1][1]
    #     sum2 += vertices[i][1] * vertices[i + 1][0]
    # sum1 += vertices[nb_vertices - 1][0] * vertices[0][1]
    # sum2 += vertices[0][0] * vertices[nb_vertices - 1][1]

    sum1 = sum(x * y for (x, _), (_, y) in zip(vertices, vertices[1:] + [vertices[0]]))
    sum2 = sum(y * x for (_, y), (x, _) in zip(vertices, vertices[1:] + [vertices[0]]))
    area = int(abs(sum1 - sum2) / 2)

    # The area is not what we are searching for, we also need the "lines" between vertices => the perimeter
    perimeter = sum(int(dist) for _, dist, *_ in data)

    result = area + (perimeter // 2 + 1)

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000_000:.2f}µs) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert execute(load_data(TEST_FILE), True) == 62
    assert execute(load_data(INPUT_FILE), True) == 76387

    assert execute(load_data(TEST_FILE), False) == 952408144115
    assert execute(load_data(INPUT_FILE), False) == 250022188522074
