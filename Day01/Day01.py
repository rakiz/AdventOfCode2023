import re

INPUT_FILE = "input.txt"
TEST1_FILE = "test1.txt"
TEST2_FILE = "test2.txt"


def process_file(filename, func):
    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line
        while line := file.readline().rstrip():
            result = func(line, result)
        return result


def part1(line, result):
    # search for digits
    findings = re.findall("\\d", line)
    # assemble the first and the last ones and convert them to integer
    number = int(findings[0] + findings[-1])
    # sum everything together
    return result + number


# conversion from letters to numbers
# trick: keep first letter if any of the following ends with it
#        same for last letter
convert_dict = {
    "zero": "0o",
    "one": "o1e",
    "two": "t2",
    "three": "t3e",
    "four": "4",
    "five": "5e",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part2(line, result):
    # convert words into digits
    for k, v in convert_dict.items():
        line = line.replace(k, v)
    return part1(line, result)


if __name__ == '__main__':
    assert (process_file(TEST1_FILE, part1) == 142)
    print('Part 1 answer : {0}'.format(process_file(INPUT_FILE, part1)))

    assert (process_file(TEST2_FILE, part2) == 281)
    print('Part 2 answer : {0}'.format(process_file(INPUT_FILE, part2)))  # expect 55686
