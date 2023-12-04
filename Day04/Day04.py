import re

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def process_file(filename, func):
    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line and call the func
        while line := file.readline().rstrip():
            result = func(line, result)

        return result


def part1(line, result):
    _, winnings, draw = re.split(r"[:|]", line)
    win_numbers = winnings.split()

    w = sum(draw_number in win_numbers for draw_number in draw.split())
    return result + 2 ** (w - 1) if w > 0 else result


winning_cards = {}


def part2(line, result):
    game_id, numbers = line.split(":")
    _, game_number = game_id.split()
    game_number = int(game_number)

    n = winning_cards.get(game_number, 0) + 1
    winning_cards[game_number] = n

    winnings, draw = numbers.split("|")
    w = sum(draw_number in winnings.split() for draw_number in draw.split())

    if w > 0:
        for i in range(w):
            winning_cards[(game_number + i + 1)] = winning_cards.get(game_number + i + 1, 0) + n

    return result + winning_cards[game_number]


if __name__ == '__main__':
    assert (process_file(TEST_FILE, part1) == 13)
    print('Part 1 answer : {0}'.format(process_file(INPUT_FILE, part1)))  # 21959

    assert (process_file(TEST_FILE, part2) == 30)
    winning_cards.clear()  # DO NOT FORGET TO CLEAN UP YOUR PLATE!
    print('Part 2 answer : {0}'.format(process_file(INPUT_FILE, part2)))  # 5132675
