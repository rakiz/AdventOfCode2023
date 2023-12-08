import re
import time

INPUT_FILE = "input.txt"
TEST1_FILE = "test1.txt"
TEST2_FILE = "test2.txt"


def process_file(filename, func):
    print("Day 01 - Start")
    t0 = time.perf_counter()
    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line, and call the func
        while line := file.readline().rstrip():
            result = func(line, result)

        t1 = time.perf_counter()
        print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
        return result


def part1(line, result):
    # search for digits
    findings = re.findall(r"\d", line)
    # assemble the first and the last ones and convert them to integer
    number = int(findings[0] + findings[-1])
    # sum everything together
    return result + number


# conversion from letters to numbers
# trick: keep first letter if any of the following ends with it, same with the last letter if following starts with it
convert_dict = {
    "zero": "0o",
    "one": "o1e",
    "two": "t2",
    "three": "t3e",
    "four": "4",
    "five": "5e",
    "six": "6",
    "seven": "7n",
    "eight": "e8",
    "nine": "9",
}


def part2(line, result):
    # convert words into digits
    for k, v in convert_dict.items():
        line = line.replace(k, v)
    return part1(line, result)


if __name__ == '__main__':
    assert process_file(TEST1_FILE, part1) == 142
    assert process_file(INPUT_FILE, part1) == 55029

    assert process_file(TEST2_FILE, part2) == 281
    assert process_file(INPUT_FILE, part2) == 55686
