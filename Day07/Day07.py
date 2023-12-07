import time
from collections import Counter

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"

PART1_CARDS_ORDER = "AKQJT98765432"
PART2_CARDS_ORDER = "AKQT98765432J"


def load_file(filename):
    hands = []
    with open(filename, 'r', encoding='UTF-8') as file:
        while line := file.readline().rstrip():
            cards, bid = line.split()  # 32T3K 765
            hands.append([cards, int(bid)])  # Don't forget to convert the bid for later !

    return hands


def hands_sort_part1(hands):
    order = "AKQJT98765432"
    return tuple(order.index(card) for card in (hands[0]))


def hands_sort_part2(hands):
    order = "AKQT98765432J"  # 'J' has now the lower value
    return tuple(order.index(card) for card in (hands[0]))


def execute(filename, is_part2):
    hands = load_file(filename)
    print(f"Day 07 - Part1 Start ({filename})")
    t0 = time.time_ns()

    hands_per_type = {}
    for hand in hands:
        card_counts = Counter(hand[0])
        if is_part2:  # /!\  difference between part1 & part2: in part2, J can replace *another* card
            # What is the most common char different from "J"?
            most_common_char = next((char for char, _ in card_counts.most_common() if char != "J"), None)
            if most_common_char:
                # We found one, let's replace it, and count again!
                joker_hand = hand[0].replace('J', most_common_char)
                card_counts = Counter(joker_hand)

        # calculate a group id, based on the occurrences of (potentially jokerized) cards, occurrences reversely ordered
        group_id = "".join(str(count) for count in sorted(card_counts.values(), reverse=True))
        # and let's put our hand (the original one, /!\ not the jokerized one /!\) in this group
        hands_per_type.setdefault(group_id, []).append(hand)

    # We can now order each group's hands by their cards value (depending on part number)
    sort_method = hands_sort_part2 if is_part2 else hands_sort_part1  # /!\ difference between part1 & part2
    sorted_groups_types = {
        key: sorted(value, key=sort_method, reverse=True) for key, value in hands_per_type.items()
    }
    # And now order the groups using their keys (increasing type value)
    sorted_groups = {key: sorted_groups_types[key] for key in sorted(sorted_groups_types)}

    result, i = 0, 1
    for group, hands in sorted_groups.items():
        for hand in hands:
            result += i * hand[1]
            i += 1

    t1 = time.time_ns()
    print("End ({}ms)- result = {}\n".format((t1 - t0) / 1000000, result))
    return result


if __name__ == '__main__':
    assert execute(TEST_FILE, False) == 6440
    assert execute(INPUT_FILE, False) == 246912307

    assert execute(TEST_FILE, True) == 5905
    assert execute(INPUT_FILE, True) == 246894760
