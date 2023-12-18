import heapq  # https://realpython.com/python-heapq-module/
import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_data(filename):
    with open(filename, "r") as file:
        data = [[int(char) for char in line.rstrip()] for line in file.readlines()]
        return data


possible_directions = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
opposite_directions = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E', 'X': 'X'}


def get_possible_moves(grid, cur_pos, dir: str, is_part1):
    new_moves = []
    # get the latest direction, and handle the case with no direction
    latest_dir = dir[-1]
    opposite_dir = opposite_directions[latest_dir]
    for i, (possible_dir, v) in enumerate(possible_directions.items()):
        # new direction cannot be opposite of latest
        if opposite_dir == possible_dir: continue
        # for part 1: No more than 3 time the same directions
        if is_part1 and len(dir) >= 3 and latest_dir == possible_dir: continue
        # for part 2: Must be at least 4 times the same direction
        if not is_part1 and len(dir) < 4 and latest_dir != possible_dir and latest_dir != 'X': continue
        # for part 2: But not more than 10 times the same direction
        if not is_part1 and len(dir) >= 10 and latest_dir == possible_dir: continue
        new_pos = (cur_pos[0] + v[0], cur_pos[1] + v[1])
        # new_pos.x or new_pos.y is not in the grid
        if not 0 <= new_pos[1] < len(grid) or not 0 <= new_pos[0] < len(grid[0]): continue
        # keep track of repeating directions, or reset it to current one only
        new_directions = possible_dir if latest_dir != possible_dir else dir + possible_dir
        new_moves.append((new_pos, new_directions))
    return new_moves


def execute(data, is_part1):
    print(f"Day 17 part {'1' if is_part1 else '2'} - Start")
    t0 = time.perf_counter()

    start = (0, (0, 0), "X")  # heat, position, directions (repeat dir)
    destination = (len(data) - 1, len(data[0]) - 1)

    # we put our starting point (with a 0 cost value) and a known-fake direction
    path = [start]
    heapq.heapify(path)
    visited = {}

    while path:
        # we always start our journey with the lowest cost (and remove it from the queue)
        cur_heat, (cur_pos), cur_dir = heapq.heappop(path)
        # We don't want to loop forever, so we'll keep track of the positions we evaluated
        # We need to keep the direction, as the next moves are impacted by it
        if (cur_pos, cur_dir) in visited: continue
        # As we always start with the cheapest cost, first tim we were the is always the cheapest => we store it
        visited[(cur_pos, cur_dir)] = cur_heat

        # let's get our *possible* next moves
        next_moves = get_possible_moves(data, cur_pos, cur_dir, is_part1)
        for next_pos, next_dir in next_moves:
            # for each of them we calculate the cost to go there, and add it to our heapq
            next_heat = cur_heat + data[next_pos[1]][next_pos[0]]
            heapq.heappush(path, (next_heat, next_pos, next_dir))

    # find the minimum heat for the destination, whatever the direction we used
    result = min(cur_heat for (cur_pos, cur_dir), cur_heat in visited.items() if cur_pos == destination)

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert execute(load_data(TEST_FILE), True) == 102
    assert execute(load_data(INPUT_FILE), True) == 684

    assert execute(load_data(TEST_FILE), False) == 94
    assert execute(load_data(INPUT_FILE), False) == 822
