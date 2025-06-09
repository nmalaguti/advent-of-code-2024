from copy import deepcopy
from functools import cache

from stdlib import *

DIRECTION_CHARS = {
    (0, -1): "^",
    (1, 0): ">",
    (0, 1): "v",
    (-1, 0): "<",
}


class Keypad:
    layout = None
    directions = DIRECTIONS

    def __init__(self):
        self.G = as_2d_graph(self.layout)
        index = graph_index(self.G)
        for gap in index[" "]:
            self.G.remove_node(gap)

        for y, row in enumerate(self.layout):
            for x, c in enumerate(row):
                if c != " ":
                    self.G.nodes[(x, y)]["value"] = c


class NumericKeypad(Keypad):
    layout = [
        "789",
        "456",
        "123",
        " 0A",
    ]
    directions = [LEFT, DOWN, RIGHT, UP]


class DirectionalKeypad(Keypad):
    layout = [" ^A", "<v>"]
    directions = [UP, RIGHT, DOWN, LEFT]


def make_paths(keypad: Keypad):
    all_paths = defaultdict(list)
    for source in keypad.G.nodes:
        for target in keypad.G.nodes:
            for path in nx.all_shortest_paths(keypad.G, source, target):
                button_presses = []
                for u, v in pairwise(path):
                    direction = Coord.direction(u, v)
                    button_presses.append(DIRECTION_CHARS[direction])
                button_presses.append("A")
                all_paths[
                    (keypad.G.nodes[source]["value"], keypad.G.nodes[target]["value"])
                ].append(button_presses)

    return all_paths


def find_all_ways(input_path: list[str], paths: dict[tuple[str, str], list[str]]):
    ways = defaultdict(list)
    for i, (source, target) in enumerate(pairwise(chain(["A"], input_path))):
        for path in paths[(source, target)]:
            ways[(source, target, i)].append(path)

    return ways


def all_possible_inputs(inputs: dict[tuple[str, str], list[str]]):
    return map(rcompose(flatten, list), product(*inputs.values()))


def part_1(lines: list[str]):
    numpad = NumericKeypad()
    all_numpad_paths = make_paths(numpad)

    dpad = DirectionalKeypad()
    all_dpad_paths = make_paths(dpad)

    re_segment = re.compile(r"(?<=A)")
    dpad_to_dpad = {}
    numpad_to_dpad = {}
    for pair, paths in all_numpad_paths.items():
        # all_paths = []
        best_path = None
        for numpad_path in paths:
            nav_options = find_all_ways(numpad_path, all_dpad_paths)
            for option in all_possible_inputs(nav_options):
                nav_options2 = find_all_ways(option, all_dpad_paths)
                dpad_path = first(all_possible_inputs(nav_options2))
                if best_path is None:
                    best_path = (dpad_path, option, numpad_path)
                elif len(best_path[0]) > len(dpad_path):
                    best_path = (dpad_path, option, numpad_path)

        dpad_path, option, numpad_path = best_path
        key = "".join(numpad_path)
        value = "".join(dpad_path)

        numpad_to_dpad[pair] = key
        dpad_to_dpad[key] = re_segment.split(value)[:-1]
        dpad_to_dpad["".join(option)] = re_segment.split(value)[:-1]

    for in_patterns in list(dpad_to_dpad.values()):
        for in_pattern in in_patterns:
            if in_pattern not in dpad_to_dpad:
                nav_options = find_all_ways(in_pattern, all_dpad_paths)
                a_path = first(all_possible_inputs(nav_options))
                dpad_to_dpad[in_pattern] = re_segment.split("".join(a_path))[:-1]

    complexity_sum = 0
    for line in lines:
        solution = []
        for source, target in pairwise(chain(["A"], line)):
            solution.append(numpad_to_dpad[(source, target)])

        key = "".join(solution)
        for i in range(1):
            next_level = []
            for pattern in solution:
                next_level.extend(dpad_to_dpad[pattern])
            dpad_to_dpad[key] = next_level
            solution = next_level
        joined = "".join(solution)
        complexity_sum += len(joined) * one(ints(line))
        dprint(line, joined)

    return complexity_sum


def part_2(lines: list[str]):
    numpad = NumericKeypad()
    all_numpad_paths = make_paths(numpad)

    dpad = DirectionalKeypad()
    all_dpad_paths = make_paths(dpad)

    re_segment = re.compile(r"(?<=A)")
    dpad_to_dpad = {}
    numpad_to_dpad = {}

    patterns = deque(all_dpad_paths.values())
    while patterns:
        paths = patterns.popleft()
        best_path = None
        for dpad_path in paths:
            options1 = find_all_ways(dpad_path, all_dpad_paths)
            for option in all_possible_inputs(options1):
                options2 = find_all_ways(option, all_dpad_paths)
                first_path = first(all_possible_inputs(options2))
                if best_path is None:
                    best_path = (first_path, option, dpad_path)
                elif len(best_path[0]) > len(first_path):
                    best_path = (first_path, option, dpad_path)

        first_path, option, dpad_path = best_path
        option_str = "".join(option)
        dpad_path_str = "".join(dpad_path)

        parts = re_segment.split(option_str)[:-1]
        dpad_to_dpad[dpad_path_str] = parts
        for part in parts:
            if part not in dpad_to_dpad:
                patterns.append([list(part)])

    for pair, paths in all_numpad_paths.items():
        best_path = None
        for numpad_path in paths:
            nav_options = find_all_ways(numpad_path, all_dpad_paths)
            for option in all_possible_inputs(nav_options):
                best_dpad_path = None
                nav_options2 = find_all_ways(option, all_dpad_paths)
                for option2 in all_possible_inputs(nav_options2):
                    nav_options3 = find_all_ways(option2, all_dpad_paths)
                    dpad_path = first(all_possible_inputs(nav_options3))

                    if best_dpad_path is None:
                        best_dpad_path = dpad_path
                    elif len(best_dpad_path) > len(dpad_path):
                        best_dpad_path = dpad_path

                if best_path is None:
                    best_path = (best_dpad_path, option, numpad_path)
                elif len(best_path[0]) > len(best_dpad_path):
                    best_path = (best_dpad_path, option, numpad_path)

        dpad_path, option, numpad_path = best_path
        key = "".join(numpad_path)
        value = "".join(option)

        numpad_to_dpad[pair] = key
        if key not in dpad_to_dpad:
            dpad_to_dpad[key] = re_segment.split(value)[:-1]

    translation = deepcopy(dpad_to_dpad)

    @cache
    def recurse(i, expansion):
        if i == 0:
            return len(expansion)
        result = 0
        for segment in expansion:
            result += recurse(i - 1, tuple(translation[segment]))
        return result

    final = {}
    for key, value in dpad_to_dpad.items():
        final[key] = recurse(25, tuple(value))

    complexity_sum = 0
    for line in lines:
        solution = []
        for source, target in pairwise(chain(["A"], line)):
            solution.append(numpad_to_dpad[(source, target)])

        total = 0
        for pattern in solution:
            total += final[pattern]
        complexity_sum += total * one(ints(line))
        dprint(line, total)

    return complexity_sum


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
