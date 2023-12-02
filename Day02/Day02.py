import operator
from functools import reduce

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def process_file(filename, func):
    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line
        while line := file.readline().rstrip():
            result = func(line, result)

        return result


bag = {"red": 12, "green": 13, "blue": 14}


def part1(line, result):
    game_split = line.split(":")
    game_num = int(game_split[0].split()[1])

    possible = True
    for draws in game_split[1].split(";"):
        cube_draws = draws.split(',')
        for cube in cube_draws:
            draw = cube.split()
            possible = possible and int(draw[0]) <= bag[draw[1]]

    return result + game_num if possible else result


def part2(line, result):
    # initialize with 0 all cube colors
    min_cubes = {"red": 0, "green": 0, "blue": 0}
    game_split = line.split(":")
    for draws in game_split[1].split(";"):
        cube_draws = draws.split(',')
        for cube in cube_draws:
            draw = cube.split()
            min_cubes[draw[1]] = max(min_cubes[draw[1]], int(draw[0]))

    return result + reduce(operator.mul, min_cubes.values(), 1)


if __name__ == '__main__':
    assert (process_file(TEST_FILE, part1) == 8)
    print('Part 1 answer : {0}'.format(process_file(INPUT_FILE, part1)))

    assert (process_file(TEST_FILE, part2) == 2286)
    print('Part 2 answer : {0}'.format(process_file(INPUT_FILE, part2)))
