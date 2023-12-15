import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_data(filename):
    with open(filename, "r") as file:
        data = [cmd for row in file.read().strip().split('\n') for cmd in row.split(",")]
        return data


def hash_me(cmd):
    h = 0
    for char in cmd:
        h = ((h + ord(char)) * 17) % 256
    return h


def part1(data):
    print("Day 15 part 1 - Start")
    t0 = time.perf_counter()

    result = 0
    for cmd in data:
        result += hash_me(cmd)

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


def part2(data):
    print("Day 15 part 2 - Start")
    t0 = time.perf_counter()

    # let's create our 256 boxes of arrays (to keep insertion order)
    boxes = [[] for _ in range(256)]
    for cmd in data:
        if cmd[-1] == "-":
            label = cmd[:-1]
            box_number = hash_me(label)
            # remove from box
            boxes[box_number] = [(la, le) for la, le in boxes[box_number] if la != label]
        elif cmd[-2] == "=":
            label = cmd[:-2]
            lens = int(cmd[-1:])
            box_number = hash_me(label)
            # search if already present
            found = False
            for i, (la, _) in enumerate(boxes[box_number]):
                if la == label:  # Found it! Let's replace it
                    boxes[box_number][i] = (label, lens)
                    found = True
                    break
            if not found:   # Not found? let's append it
                boxes[box_number].append((label, lens))
        else:
            print(f"Houston! We've got a problem! This was not expected!\n"
                  f"Last char is neither a '-' nor the one before a '=' => {cmd}")

    result = 0
    for i, box in enumerate(boxes, start=1):
        for j, (_, lens) in enumerate(box, start=1):
            result += i * j * lens

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert part1(load_data(TEST_FILE)) == 1320
    assert part1(load_data(INPUT_FILE)) == 511257

    assert part2(load_data(TEST_FILE)) == 145
    assert part2(load_data(INPUT_FILE)) == 239484
