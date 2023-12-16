import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_data(filename):
    with open(filename, "r") as file:
        data = [line.rstrip() for line in file.readlines()]
        return data


NORTH, EST, SOUTH, WEST = 0, 1, 2, 3
mirror_direction_to_directions = {
    '.': [[NORTH], [EST], [SOUTH], [WEST]],
    '/': [[EST], [NORTH], [WEST], [SOUTH]],
    '\\': [[WEST], [SOUTH], [EST], [NORTH]],
    '|': [[NORTH], [NORTH, SOUTH], [SOUTH], [NORTH, SOUTH]],
    '-': [[EST, WEST], [EST], [EST, WEST], [WEST]]
}

# for each direction, how do we move on x and on y
# north, east, south, west
directions_x = [0, 1, 0, -1]
directions_y = [-1, 0, 1, 0]


# def next_move_recursive(data, beams, start_x, start_y, direction):
#     # stop conditions
#     if start_x < 0 or start_x >= len(data[0]) or start_y < 0 or start_y >= len(data):
#         return
#     # memoization: avoid infinite loops
#     if (start_x, start_y) in beams and direction in beams[(start_x, start_y)]:
#         return
#     beam = beams.setdefault((start_x, start_y), [])
#     beam.append(direction)
#
#     m = data[start_y][start_x]
#     next_directions = mirror_direction_to_directions[m][direction]
#     for next_direction in next_directions:
#         # apply next direction
#         next_x = start_x + directions_x[next_direction]
#         next_y = start_y + directions_y[next_direction]
#         # and lets loop!
#         next_move_recursive(data, beams, next_x, next_y, next_direction)
#
#     return


def next_move(data, paths):
    beams = {}
    while len(paths) > 0:
        new_paths = []
        for start_x, start_y, direction in paths:
            # stop conditions
            if start_x < 0 or start_x >= len(data[0]) or start_y < 0 or start_y >= len(data):
                continue
            # memoization: avoid infinite loops
            if (start_x, start_y) in beams and direction in beams[(start_x, start_y)]:
                continue

            beam = beams.setdefault((start_x, start_y), [])
            beam.append(direction)

            m = data[start_y][start_x]
            next_directions = mirror_direction_to_directions[m][direction]
            for next_direction in next_directions:
                # apply next direction
                next_x = start_x + directions_x[next_direction]
                next_y = start_y + directions_y[next_direction]
                new_paths.append((next_x, next_y, next_direction))
        paths = new_paths

    return len(beams)


# def part1_recursive(data):
#     print("Day 15 part 1 (recursive) - Start")
#     t0 = time.perf_counter()
#
#     beams = {}
#     next_move_recursive(data, beams, 0, 0, 1)
#     result = len(beams)
#
#     t1 = time.perf_counter()
#     print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
#     return result


def part1(data):
    print("Day 15 part 1 - Start")
    t0 = time.perf_counter()

    result = next_move(data, [(0, 0, EST)])

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


def part2(data):
    print("Day 15 part 2 - Start")
    t0 = time.perf_counter()
    result = 0

    for x in range(len(data[0])):
        result = max(result, next_move(data, [(x, 0, SOUTH)]))
        result = max(result, next_move(data, [(x, len(data) - 1, NORTH)]))
    for y in range(len(data)):
        result = max(result, next_move(data, [(0, y, EST)]))
        result = max(result, next_move(data, [(len(data[0]) - 1, y, WEST)]))

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert part1(load_data(TEST_FILE)) == 46
    # assert part1_recursive(load_data(TEST_FILE)) == 46
    assert part1(load_data(INPUT_FILE)) == 6994
    # assert part1_recursive(load_data(INPUT_FILE)) == 6994

    assert part2(load_data(TEST_FILE)) == 51
    assert part2(load_data(INPUT_FILE)) == 7488
