import re

FILENAME = "input.txt"


def process_file(filename, func):
    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line
        while line := file.readline().rstrip():
            result = func(line, result)
        return result


def part1inner(line, result):
    # search for digits
    findings = re.findall("\d", line)
    # assemble the first and the last ones and convert them to integer
    number = int(findings[0] + findings[-1])
    # sum everything together
    return result + number


# conversion from letters to numbers
# trick: keep start and end letters if they can end or start other number names
convert_dict = {
    "zero": "_0o",   # => X / One
    "one": "o1e",    # => zerO / Eight
    "two": "t2o",    # => eighT / One
    "three": "t3_",  # => eighT / Eight
    "four": "_4_",   # => X / X
    "five": "_5e",   # => X / Eight
    "six": "_6_",    # => X / X
    "seven": "_7_",  # => X / X
    "eight": "e8t",  # => onE, threE / Two, Three
    "nine": "_9e",   # => X / Eight
}


def part2inner(line, result):
    # convert words into digits
    for k, v in convert_dict.items():
        line = line.replace(k, v)
    return part1inner(line, result)


if __name__ == '__main__':
    print('part 1 sum : {0}'.format(process_file(FILENAME, part1inner)))  # expect 55029
    print('part 2 sum : {0}'.format(process_file(FILENAME, part2inner)))  # expect 55686
