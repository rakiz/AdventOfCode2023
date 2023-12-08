import math
import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


# returns [(time,distance to beat),...]
def get_data(filename, is_part1):
    races = []
    with open(filename, 'r', encoding='UTF-8') as file:
        # Times
        _, *times = file.readline().rstrip().split()
        _, *distances = file.readline().rstrip().split()
        if is_part1:
            for i in range(len(times)):
                races.append((int(times[i]), int(distances[i])))
        else:
            race_time = ""
            distance = ""
            for i in range(len(times)):
                race_time += times[i]
                distance += distances[i]
            races.append((int(race_time), int(distance)))

    return races


def execute(races):
    print(f"Day 05 - Start - races: {races}")
    t0 = time.perf_counter()
    result = 1  # not 0, we're multiplying here !
    for race_time, distance in races:
        # x is the race_time we press the button
        # distance < (race_time - x) * x  =>  distance < race_time*x - x*x
        # =>   x² - race_time*x + distance < 0  (ax²+bx+c=0)
        a, b, c = 1, -race_time, distance
        # √D = √(race_time²−4*distance)    √(b²-4ac)
        racine_delta = math.sqrt(b * b - 4 * a * c)
        # solutions: (-race_time +/- √D) / 2         (-b +/- √D) / 2a
        # trick: add epsilon value and ceil min solution; sub epsilon value and floor max solution
        solution1 = math.floor(((-b - racine_delta) / 2)) + 1
        solution2 = math.ceil(((-b + racine_delta) / 2)) - 1
        # multiplying with the number of ways to beat it
        result *= solution2 - solution1 + 1

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000_000:.2f}µs) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert execute(get_data(TEST_FILE, True)) == 288
    assert execute(get_data(INPUT_FILE, True)) == 114400

    assert execute(get_data(TEST_FILE, False)) == 71503
    assert execute(get_data(INPUT_FILE, False)) == 21039729
