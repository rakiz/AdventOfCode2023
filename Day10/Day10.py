import time

# TODO: Cleanup this !!
INPUT_FILE = "input.txt"
TEST1_FILE = "test1.txt"
TEST2_FILE = "test2.txt"
TEST3_FILE = "test3.txt"

L = 0
C = 1


def load_file(filename):
    with open(filename, "r") as file:
        data = file.read().split('\n')

    return data


def find_start(data):
    for lig, pipes in enumerate(data):
        for col, pipe in enumerate(pipes):
            if pipe == "S":
                return lig, col
    return None


def value(pipes, pos):
    return pipes[pos[L]][pos[C]] if 0 <= pos[L] < len(pipes) and 0 <= pos[C] < len(pipes[0]) else None


map_pipe_to_vectors = {
    'S': [(0, -1), (0, +1), (-1, 0), (+1, 0)],
    '|': [(-1, 0), (+1, 0)],
    '-': [(0, -1), (0, +1)],
    'L': [(-1, 0), (0, +1)],
    'J': [(-1, 0), (0, -1)],
    '7': [(0, -1), (+1, 0)],
    'F': [(0, +1), (+1, 0)],
    '.': [(0, 0)]
}


def possible_moves(pipes, from_pos, pos):
    pipe = value(pipes, pos)
    possible_next = [(pos[L] + move[L], pos[C] + move[C]) for move in (map_pipe_to_vectors[pipe])]

    if pipe == 'S':
        filtered = [pn for pn in possible_next if from_pos in possible_moves(pipes, pn, pn)]
    else:
        # Filter out moves that are Invalid, destination values that are None, and start position
        filtered = [pn for pn in possible_next if pn is not None and value(pipes, pn) is not None and pn != from_pos]

    return filtered


def execute(filename):
    print(f"Day 10 ({filename}) - Start")
    t0 = time.perf_counter()

    original_board = load_file(filename)
    trace_board = [[False] * len(original_board[0]) for _ in range(len(original_board))]

    start = find_start(original_board)
    trace_board[start[0]][start[1]] = True

    next_positions = [(start, pm) for pm in possible_moves(original_board, start, start)]
    count_part1 = 1
    while True:
        new_next_positions = []
        count_part1 += 1
        for old_pos, new_pos in next_positions:
            trace_board[new_pos[0]][new_pos[1]] = True
            next_old_pos = new_pos
            next_new_pos = possible_moves(original_board, old_pos, new_pos)
            new_next_positions.append((next_old_pos, next_new_pos[0]))

        if new_next_positions[0][1] == new_next_positions[1][1]:
            trace_board[next_new_pos[0][0]][next_new_pos[0][1]] = True
            break
        next_positions = new_next_positions

    count_part2 = 0
    for lig in range(len(trace_board)):
        # we'll evaluate if the pipe is changing the status (in/out) for next line
        inside = False
        for col in range(len(trace_board[0])):
            if trace_board[lig][col]:  # This pos is part of the path
                # Handle the case of 'S'
                # -> if we have an "S" and above a south connection, we must act as a north connection
                here = original_board[lig][col]
                above = original_board[lig - 1][col] if lig > 0 and here == 'S' else 'S'
                if here in "|JL" or above in "|7F": inside = not inside
            else:
                if inside: count_part2 += 1

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}s) - result for part1 = {count_part1} and for part2 = {count_part2}\n")
    return count_part1, count_part2


if __name__ == '__main__':
    assert execute(TEST1_FILE) == (4, 1)
    assert execute(TEST2_FILE) == (23, 4)
    assert execute(INPUT_FILE) == (6701, 303)
