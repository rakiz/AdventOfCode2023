import time
from hmac import new

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_data(filename):
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file]
        # return [line.strip() for line in file.readlines()]


def print_board(board):
    print("-" * len(board[0]))
    for row in board:
        print("".join(row))


def get_shape(board):
    return ''.join(''.join(row) for row in board)


def count_load(board):
    result = 0
    for m, row in enumerate(board):
        result += (len(board) - m) * row.count('O')
    return result


def roll_north(board):
    last_blockers = [-1] * len(board[0])
    new_board = []
    for r, row in enumerate(board):
        new_board_line = ['?'] * len(row)  # let's create a destination line
        for c, cell in enumerate(row):
            new_cell = cell
            if cell == '#':  # a new blocker for this column
                last_blockers[c] = r  # WE are the blocker!
            elif cell == "O":
                if last_blockers[c] + 1 < r:  # rollin' rollin' rollin'
                    last_blockers[c] += 1  # We'll move the rock, and we'll become the new blocker
                    new_board[last_blockers[c]][c] = cell  # Here! We have to update a previous line
                    new_cell = '.'  # and our current line will become a '.'
                else:
                    last_blockers[c] = r  # We're not moving, and we become the new blocker
            new_board_line[c] = new_cell
        new_board.append(new_board_line)
    return new_board


def part1(data):
    print("Day 14 part 1 - Start")
    t0 = time.perf_counter()

    new_board = roll_north(data)
    result = count_load(new_board)

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


def part2(data, nb_cycles):
    print("Day 14 part 2 - Start")
    t0 = time.perf_counter()

    new_board, cur_cycles = data, 0
    cycle_per_board_shape = {}
    while cur_cycles < nb_cycles:
        for _ in range(4):  # 4 roll for a cycle
            # roll everything to (current) north
            new_board = roll_north(new_board)
            # rotate clockwise, so north becomes west, etc...
            new_board = [list(row) for row in zip(*new_board[::-1])]

        board_shape = get_shape(new_board)
        if board_shape in cycle_per_board_shape:  # We already went there, let's extrapolate
            # Let's calculate the size of the repeated pattern
            size_of_pattern = cur_cycles - cycle_per_board_shape[board_shape]
            # And how many times it will be completely repeating it in the remaining cycles
            nb_complete_patterns = (nb_cycles - cur_cycles) // size_of_pattern
            # And now let's cheat and jump in a future cycle
            cur_cycles += nb_complete_patterns * size_of_pattern

        cycle_per_board_shape[board_shape] = cur_cycles
        cur_cycles += 1

    result = count_load(new_board)

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert part1(load_data(TEST_FILE)) == 136
    assert part1(load_data(INPUT_FILE)) == 108840

    assert part2(load_data(TEST_FILE), 1_000_000_000) == 64
    assert part2(load_data(INPUT_FILE), 1_000_000_000) == 103445
