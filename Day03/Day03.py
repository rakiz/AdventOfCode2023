import re
import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def preprocess_file(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        lines = [line.rstrip() for line in file.readlines()]

        numbers = [[match for match in re.finditer(r'\d+', line)] for line in lines]
        symbols = [[match for match in re.finditer(r'[^0-9.]', line)] for line in lines]

    return numbers, symbols


def get_adjacent(multiples, unique, i):
    result = []
    multiples_start = max(i - 1, 0)
    multiples_end = min(i + 1, len(multiples))
    for line in multiples[multiples_start:multiples_end + 1]:
        for item in line:
            if ((unique.start() <= item.end() and unique.end() >= item.start())
                    or (item.start() <= unique.end() and item.end() >= unique.start())):
                result.append(item.group())
    return result


def part1(filename):
    print("Day 03 Part1 - Start")
    t0 = time.perf_counter()
    numbers, symbols = preprocess_file(filename)

    result = 0
    for i, number_line in enumerate(numbers):
        for number in number_line:
            if len(get_adjacent(symbols, number, i)) > 0:
                result += int(number.group())

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000_000:.2f}µs) - result = {result}\n")
    return result


def part2(filename):
    print("Day 03 Part2 - Start")
    t0 = time.perf_counter()
    numbers, symbols = preprocess_file(filename)

    result = 0
    for i, symbol_line in enumerate(symbols):
        for symbol in symbol_line:
            adjacent_numbers = get_adjacent(numbers, symbol, i)
            if symbol.group() == "*" and len(adjacent_numbers) == 2:
                result += int(adjacent_numbers[0]) * int(adjacent_numbers[1])

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000_000:.2f}µs) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert part1(TEST_FILE) == 4361
    assert part1(INPUT_FILE) == 539433

    assert part2(TEST_FILE) == 467835
    assert part2(INPUT_FILE) == 75847567
