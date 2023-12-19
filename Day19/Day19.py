import re
import time

INPUT_FILE = "input.txt"
TEST_FILE = "test.txt"


def load_file(filename):
    with open(filename, "r") as file:
        flows_lines, parts_lines = [x.split("\n") for x in file.read().strip().split('\n\n')]

        return flows_lines, parts_lines


# Define the pattern for extracting flow name and rules
EXTRACT_FLOW_PATTERN = re.compile(r'(\w+){([^}]*)}')


# flows => px{a<2006:qkq,m>2090:A,rfg}
# => 'px': [(('a', '<', 2006), 'qkq'), (('m', '>', 2090), 'A'), (None, 'rfg')]
def extract_flows(flow_string):
    for flow_name, rules_str in EXTRACT_FLOW_PATTERN.findall(flow_string):
        rules = []
        for rule_str in rules_str.split(','):
            if ':' in rule_str:
                rule, value = rule_str.split(':', 1)
                test = (rule[0], rule[1], int(rule[2:]))
            else:
                test = None
                value = rule_str
            rules.append((test, value))
        return flow_name, rules
    return None, None


# parts  => {x=787,m=2655,a=1222,s=2876}
# => {'a': 1222, 'm': 2655, 's': 2876, 'x': 787}
def extract_parts(part_string):
    parts = {}
    for part in part_string[1:-1].split(','):
        k, v = part.split('=')
        parts[k] = int(v)
    return parts


def part1(filename):
    print(f"Day 19 part1 ({filename}) - Start")
    t0 = time.perf_counter()

    flows_lines, parts_lines = load_file(filename)
    # The flow map is associating each flow steps (or rules) to the name of the flow
    flow_map = {flow_name: flow for flow_name, flow in (extract_flows(flow_string) for flow_string in flows_lines)}
    result = 0
    for parts in parts_lines:
        part = extract_parts(parts)

        flow_key = 'in'  # we're starting at 'in'
        while flow_key != 'A' and flow_key != 'R':  # we keep following the flow until we reach an final state
            flow_steps = flow_map[flow_key]  # once we found out flow steps
            for cond, dest in flow_steps:  # we go over each one of them
                if cond:  # if there's a condition to get to the next flow
                    pv = part[cond[0]]
                    if (cond[1] == '<' and pv < cond[2]) or (cond[1] == '>' and pv > cond[2]):  # Then we evaluate it
                        flow_key = dest  # we are now in next flow
                        break  # no need to continue with the steps of this flow
                else:  # if there' no more condition
                    flow_key = dest  # we can jump to next flow

        # For each part, we reach a final state. If it is accepted, then we accumulate the sum of parts values
        if flow_key == 'A':
            result += sum(part.values())

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000_000:.2f}µs) - result = {result}\n")
    return result


def part2(filename):
    print(f"Day 19 part2 ({filename}) - Start")
    t0 = time.perf_counter()

    # we don't care about the parts from the file, as we'll have to handle ranges of them
    flows_lines, _ = load_file(filename)
    # So we'll start with the flow 'in' and with full ranges on all parts
    parts_ranges = [('in', {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]})]
    # The flow map is associating each flow steps (or rules) to the name of the flow
    flow_map = {flow_name: flow for flow_name, flow in (extract_flows(flow_string) for flow_string in flows_lines)}

    result = 0
    # we'll keep going as long as there are ranges or parts not reaching a final state
    while len(parts_ranges) > 0:
        new_parts_range = []
        for flow_key, part in parts_ranges:
            # in case we reach a final state, either skip it, or calculate its piece of the final result
            if flow_key == 'R': continue  # rejected group!
            if flow_key == 'A':  # accepted group! let's calculate how many
                sr = 1
                for r in part.values(): sr *= r[1] - r[0] + 1  # multiply ranges to add to the result
                result += sr
                continue
            # let's get all the steps/rules of the flow
            flow_steps = flow_map[flow_key]
            for cond, dest in flow_steps:
                new_part = part.copy()
                if cond:  # if we get a condition, we split the part range in 2
                    pv = part[cond[0]]
                    if cond[1] == '<':
                        new_part[cond[0]] = [pv[0], cond[2] - 1]  # the part fulfilling the rule
                        part[cond[0]] = [cond[2], pv[1]]  # the part that will be evaluated on next step
                    elif cond[1] == '>':
                        part[cond[0]] = [pv[0], cond[2]]  # the part that will be evaluated on next step
                        new_part[cond[0]] = [cond[2] + 1, pv[1]]  # the part fulfilling the rule
                new_parts_range.append((dest, new_part))  # we keep it for next round, as these will match another flow
        parts_ranges = new_parts_range

    t1 = time.perf_counter()
    print(f"End ({(t1 - t0) * 1_000:.2f}ms) - result = {result}\n")
    return result


if __name__ == '__main__':
    assert part1(TEST_FILE) == 19114
    assert part1(INPUT_FILE) == 362930

    assert part2(TEST_FILE) == 167409079868000
    assert part2(INPUT_FILE) == 116365820987729
