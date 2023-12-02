import operator
from functools import reduce

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def process_file(filename, func):
    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line and call the func
        while line := file.readline().rstrip():
            result = func(line, result)

        return result


bag = {"red": 12, "green": 13, "blue": 14}


def part1(line, result):
    game_id, game_draws = line.split(":")
    _, game_num = game_id.split()

    for draws in game_draws.split(";"):
        cube_draws = draws.split(',')
        for cube in cube_draws:
            number, color = cube.split()
            # Hey! Wait! For this color, we've drawn more cubes than there are in the bag! No need to continue.
            if int(number) > bag[color]:
                return result

    return result + int(game_num)


def part2(line, result):
    # initialize with 0 all cube colors
    min_cubes = {"red": 0, "green": 0, "blue": 0}
    _, game_draws = line.split(":")

    for draws in game_draws.split(";"):
        cube_draws = draws.split(',')
        for cube in cube_draws:
            number, color = cube.split()
            min_cubes[color] = max(min_cubes[color], int(number))

    return result + reduce(operator.mul, min_cubes.values(), 1)


if __name__ == '__main__':
    assert (process_file(TEST_FILE, part1) == 8)
    print('Part 1 answer : {0}'.format(process_file(INPUT_FILE, part1)))

    assert (process_file(TEST_FILE, part2) == 2286)
    print('Part 2 answer : {0}'.format(process_file(INPUT_FILE, part2)))
