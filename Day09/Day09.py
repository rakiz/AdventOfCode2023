import re
import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def process_file(filename, func):
    print("Day 09 - Start")
    t0 = time.perf_counter()
    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line, and call the func
        while line := file.readline().rstrip():
            numbers = list(map(int, line.split()))
            result = func(numbers, result)

        t1 = time.perf_counter()
        print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
        return result


def part1(sensors, result):
    stack = []
    while len(sensors) > 1:
        # keep the last value of the list (we'll need to add it to the diff to extrapolate)
        stack.append(sensors[-1])
        # calculate the diff between each values of the array, and make them the next array to use
        sensors = [sensors[i + 1] - sensors[i] for i in range(len(sensors) - 1)]

    # now, we have a stack with the last value of each lines of diff, just sum them up
    return result + sum(stack)


def part2(sensors, result):
    # extrapolating the beginning is like extrapolate the end of the reversed values
    return part1(sensors[::-1], result)


if __name__ == '__main__':
    assert process_file(TEST_FILE, part1) == 114
    assert process_file(INPUT_FILE, part1) == 1762065988

    assert process_file(TEST_FILE, part2) == 2
    assert process_file(INPUT_FILE, part2) == 1066
