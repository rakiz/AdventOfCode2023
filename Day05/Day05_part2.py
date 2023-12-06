import time
import re

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def apply_mapping(current_mapping, seeds):
    mapped_seeds = []
    i = 0
    while i < len(seeds):
        seed_start, seed_end = seeds[i]

        for mapping in current_mapping:
            mapping_start, mapping_end, convert = mapping
            if seed_start < mapping_start <= seed_end:
                if seed_end <= mapping_end:
                    #     |---- mapping ---|
                    #  |- seed -|
                    seeds[i] = (seed_start, mapping_start - 1)  # we need to search this one again elsewhere
                    mapped_seeds.append((mapping_start + convert, seed_end + convert))  # converted
                else:
                    #    |- mapping -|
                    #  |---- seed -----|
                    seeds[i] = (seed_start, mapping_start - 1)  # we need to search this one again elsewhere
                    mapped_seeds.append((mapping_start + convert, mapping_end + convert))  # converted
                    seeds.insert(i + 1, (mapping_end + 1, seed_end))  # we need to add a new range to convert
            elif mapping_start <= seed_start <= mapping_end:
                if seed_end <= mapping_end:
                    # |---- mapping ---|
                    #    |- seed --|
                    mapped_seeds.append((seed_start + convert, seed_end + convert))  # converted
                    seeds.pop(i)  # /!\ need to remove it from the initial seeds
                    i -= 1  # /!\  do not forget to rewind
                    break  # /!\ and to start searching mapping from the beginning, or we'll miss a seed !!
                else:
                    # |- mapping -|
                    #        |- seed -|
                    mapped_seeds.append((seed_start + convert, mapping_end + convert))  # converted
                    seeds[i] = (mapping_end, seed_end - 1)  # we need to search this one again elsewhere

            seed_start, seed_end = seeds[i]  # Do not forget to reload the modified value before next mapping round !!

        i += 1

    # the result are all the seed ranges we couldn't map (still in seeds)
    # plus the converted ranges we created on the fly (in mapped_seeds)
    seeds.extend(mapped_seeds)
    return seeds


def process_file_part2(filename):
    print("Day 05 - Part2 Start")
    t0 = time.time_ns()
    seeds = []
    current_mapping = []
    with (open(filename, 'r', encoding='UTF-8') as file):
        for line in file:
            line = line.strip()

            if len(seeds) == 0:
                # We first need to load the initial seeds, and convert them to int (Grumbl!)
                # print("Loading Seeds")
                tmp = re.split(r"[:\s]", line)
                tmp = [int(element) for element in tmp[2:]]  # tmp[2:] to ignore 'seed:' and ''
                # transform the seeds to get [start, end[, and sort them
                for i in range(0, len(tmp), 2):
                    seeds.append((tmp[i], tmp[i] + tmp[i + 1] - 1))
                # print("Seeds: {}".format(seeds))
                continue

            if line.isspace():
                continue

            mapping_entry = line.split()
            if len(mapping_entry) == 3:  # we have what we want
                # lets name and convert them, so I won't spend another hour fighting with types...
                dst_start = int(mapping_entry[0])
                src_start = int(mapping_entry[1])
                length = int(mapping_entry[2])
                src_end = src_start + length - 1
                convert = dst_start - src_start
                current_mapping.append((src_start, src_end, convert))
            elif len(current_mapping) > 0:  # This must be the start of the next mapping block
                # We have a mapping, let's apply it right now, and clear it for next round
                # We now have transformed to original seeds into their mapped version
                seeds = apply_mapping(current_mapping, seeds)
                current_mapping.clear()

        # mapping application is triggered by new block of mapping, so we must not forget the last one
        seeds = apply_mapping(current_mapping, seeds)
        # final result is the minimal low range of mapped seeds
        result = min([seed[0] for seed in seeds])
        t1 = time.time_ns()
        print("Part 2 End ({}µs)- result = {}".format((t1 - t0) / 1000, result))
        return result


if __name__ == '__main__':
    assert process_file_part2(TEST_FILE) == 46
    process_file_part2(INPUT_FILE)  # 148041808
