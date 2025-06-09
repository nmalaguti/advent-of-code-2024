from functools import total_ordering
from typing import Any

from stdlib import *


@total_ordering
class Page:
    def __init__(self, val, order):
        self.val = val
        self.order = order

    def __eq__(self, other: Any) -> bool:
        return self.val == other.val

    def __lt__(self, other: Any) -> bool:
        for rule in self.order:
            left, right = ints(rule)
            if self.val == left and other.val == right:
                return True

        return False


def part_1(lines: list[str]):
    rules = list(takewhile(bool, lines))
    rest = lines[len(rules) + 1 :]

    middles = []

    for ids in rest:
        nums = ints(ids)
        pages = [Page(num, rules) for num in nums]
        if pages == list(sorted(pages)):
            middles.append(pages[len(pages) // 2].val)

    return sum(middles)


def part_2(lines: list[str]):
    rules = list(takewhile(bool, lines))
    rest = lines[len(rules) + 1 :]

    middles = []

    for ids in rest:
        nums = ints(ids)
        pages = [Page(num, rules) for num in nums]
        ordered = list(sorted(pages))
        if pages != ordered:
            middles.append(ordered[len(ordered) // 2].val)

    return sum(middles)


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
