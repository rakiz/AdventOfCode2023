import time
import collections
import re
import sys

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_file(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        data = file.readlines()

    block_id, seeds = map(str.split, re.split(r":\s", data[0]))

    seeds_tuple = []
    for i in range(0, len(seeds), 2):
        seeds_tuple.append((int(seeds[i]), int(seeds[i]) + int(seeds[i + 1])))

    mapping = []
    current_mapping = []
    for line in data[1:]:
        if line.isspace():
            continue
        if ":" in line:
            current_mapping = collections.defaultdict()
            mapping.append(current_mapping)
            continue

        dst_start, src_start, length = line.split()
        current_mapping[int(src_start)] = [int(src_start) + int(length), int(dst_start)]

    return seeds, seeds_tuple, mapping


def find_mapping(seed, mapping):
    for src_start in sorted(mapping.keys()):
        src_end, dst_start = mapping[src_start]
        if src_start <= seed < src_end:
            return seed - src_start + dst_start
    return seed


def part1(seeds, mappings):
    print("Day 05 - Part1 Start - seeds: {}".format(seeds))
    t0 = time.time_ns()
    result = sys.maxsize
    for start in seeds:
        for mapping in mappings:
            start = find_mapping(int(start), mapping)
        result = min(start, result)
    t1 = time.time_ns()
    print("Part 1 End ({}ms)- result = {}\n".format((t1 - t0)/1000, result))
    return result


""" Not improving performances!
def merge_seeds(seeds):
    sorted_seeds = sorted(seeds)
    merged_seeds = [sorted_seeds[0]]
    for current_start, current_end in sorted(seeds)[1:]:
        previous_start, previous_end = merged_seeds[-1]

        if current_start <= previous_end:
            # starts before previous one ends, let's update our current range+
            merged_seeds[-1] = (previous_start, max(current_end, previous_end))
        else:
            # no overlap, we keep it as-is
            merged_seeds.append((current_start, current_end))

    print("part2 for merged_seeds {}".format(merged_seeds))
    return merged_seeds
"""


def part2(seeds_tuple, mappings):
    print("Day 05 - Part2 Start - seeds: {}".format(seeds_tuple))
    t0 = time.time_ns()
    min_location = sys.maxsize
    for mapping in mappings[-1].values():
        min_location = min(min_location, mapping[0])

    result = sys.maxsize
    for seeds_start, seeds_end in seeds_tuple:
        for seed in range(seeds_start, seeds_end):
            for mapping in mappings:
                seed = find_mapping(seed, mapping)
            if seed == min_location:
                return seed
            else:
                result = min(seed, result)
    t1 = time.time_ns()
    print("Part 2 End ({}ms)- result = {}".format((t1 - t0)/1000, result))
    return result


if __name__ == '__main__':
    test_seeds, test_seeds_tuple, test_mapping = load_file(TEST_FILE)
    input_seeds, input_seeds_tuple, input_mapping = load_file(INPUT_FILE)

    assert part1(test_seeds, test_mapping) == 35
    part1(input_seeds, input_mapping)  # 214922730

    assert part2(test_seeds_tuple, test_mapping) == 46
    part2(input_seeds_tuple, input_mapping)  # 148041808
