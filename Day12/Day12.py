import time
from typing import Callable

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def process_file(filename: str, func: Callable[[str, int], int]) -> int:
    print("Day 12 - Start")
    t0 = time.perf_counter()

    with open(filename, 'r', encoding='UTF-8') as file:
        result = 0
        # read the input file, line by line and call the func
        while line := file.readline().rstrip():
            result = func(line, result)
            # break

        t1 = time.perf_counter()
        print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
        return result


def recursive_count(already_computed, statuses: str, groups: tuple[int, ...]) -> int:
    # statuses => '..??.###'    /     groups => (1,1,3)
    if (statuses, groups) in already_computed:
        return already_computed[(statuses, groups)]

    result = 0

    # No more statuses we are done!
    if len(statuses) == 0:
        # oh wait, it's a solution if we don't have more groups!
        result = 1 if not len(groups) > 0 else 0
    else:
        match statuses[0]:
            # this must be part of a group
            case '#':
                # if we don't have more groups
                # or we have less cells in statuses than the size of the group,
                # or there's a '.' int the next cells forbidding it to be the next group
                if (len(groups) == 0 or
                        len(statuses) < groups[0] or
                        any(status == "." for status in statuses[0:groups[0]])):
                    pass
                # we have 2 cases:
                # Not the last group? We must be sure that we don't have enough '#' or '?' but not another '#' after
                elif len(groups) > 1:
                    if len(statuses) < groups[0] + 1 or statuses[groups[0]] == "#":
                        pass
                    else:
                        # So far, everything's fine, statuses fit the current group.
                        # Let's continue and see if this is a valid solution
                        result = recursive_count(already_computed, statuses[groups[0] + 1:], groups[1:])
                else:
                    # And the case of the last group
                    result = recursive_count(already_computed, statuses[groups[0]:], groups[1:])
            case '?':
                # '?' can be either a '#' or a '.' so let's try both possibilities
                sharp = recursive_count(already_computed, '#' + statuses[1:], groups)
                dot = recursive_count(already_computed, '.' + statuses[1:], groups)
                result = dot + sharp
            case ".":
                # let's remove all starting points at once, instead of looping here to remove them one by one
                result = recursive_count(already_computed, statuses.strip('.'), groups)

    already_computed[(statuses, groups)] = result
    return result


def part1(line: str, result: int) -> int:
    statuses, groups_s = line.split()
    groups: tuple[int, ...] = tuple(map(int, groups_s.split(',')))
    new_result = recursive_count({}, statuses.strip('.'), groups)  # remove leading and ending '.' as there are useless
    # print(f"line:'{line}' statuses:'{statuses}' cont:'{groups}' => result={new_result}")
    return result + new_result


def part2(line: str, result: int) -> int:
    statuses, groups_s = line.split()
    statuses = "?".join([statuses] * 5)  # This is part 2
    groups_s = ",".join([groups_s] * 5)  # This is part 2
    groups: tuple[int, ...] = tuple(map(int, groups_s.split(',')))
    new_result = recursive_count({}, statuses.strip('.'), groups)  # remove leading and ending '.' as there are useless
    # print(f"line:'{line}' statuses:'{statuses}' cont:'{groups}' => result={new_result}")
    return result + new_result


if __name__ == '__main__':
    assert process_file(TEST_FILE, part1) == 21
    assert process_file(INPUT_FILE, part1) == 7_379

    assert process_file(TEST_FILE, part2) == 525_152
    assert process_file(INPUT_FILE, part2) == 7_732_028_747_925
