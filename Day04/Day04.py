import re
import time
from collections import defaultdict

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def process_file(filename, func):
    print("Day 04 - Start")
    t0 = time.perf_counter()

    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line and call the func
        while line := file.readline().rstrip():
            result = func(line, result)

        t1 = time.perf_counter()
        print(f"End ({(t1 - t0) * 1_000_000:.2f}µs) - result = {result}\n")
        return result


def part1(line, result):
    _, winnings, draw = re.split(r"[:|]", line)
    w = len(set(winnings.split()) & set(draw.split()))
    return result + 2 ** (w - 1) if w > 0 else result


winning_cards = defaultdict(int)


def part2(line, result):
    game, winnings, draw = re.split(r"[:|]", line)
    _, game_number = game.split()
    game_number = int(game_number)

    winning_cards[game_number] = winning_cards.setdefault(game_number, 0) + 1
    for i in range(len(set(winnings.split()) & set(draw.split()))):
        winning_cards[(game_number + i + 1)] += winning_cards[game_number]

    return result + winning_cards[game_number]


if __name__ == '__main__':
    assert process_file(TEST_FILE, part1) == 13
    assert process_file(INPUT_FILE, part1) == 21959

    assert process_file(TEST_FILE, part2) == 30
    winning_cards.clear()  # DO NOT FORGET TO CLEAN UP YOUR PLATE!
    assert process_file(INPUT_FILE, part2) == 5132675
