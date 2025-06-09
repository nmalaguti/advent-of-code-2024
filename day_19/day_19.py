from functools import cache

from stdlib import *


def part_1(lines: list[str]):
    towels = list(lines[0].split(", "))
    regexp = re.compile(rf"^({'|'.join(towels)})*$")

    return sum(1 for design in lines[2:] if regexp.match(design))


def part_2(lines: list[str]):
    towels = set(lines[0].split(", "))

    @cache
    def count_paths_from(target, i):
        if i == len(target):
            return 1  # One valid way to reach the end
        total = 0
        for j in range(i + 1, len(target) + 1):
            substr = target[i:j]
            if substr in towels:
                total += count_paths_from(target, j)
        return total

    total_designs = 0
    for design in lines[2:]:
        total_designs += count_paths_from(design, 0)

    return total_designs


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
