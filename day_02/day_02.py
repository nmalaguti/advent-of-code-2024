from typing import Iterator

from stdlib import *


def part_1(lines: list[str]):
    def is_safe(levels: list[int]) -> bool:
        increasing = None
        for a, b in windowed(levels, 2):
            if increasing is None:
                increasing = b > a

            if increasing and a >= b:
                return False

            if not increasing and b >= a:
                return False

            if abs(a - b) > 3:
                return False

        return True

    safe_sum = 0

    for line in lines:
        if is_safe(ints(line)):
            safe_sum += 1

    return safe_sum


def permutations(levels: list[int]) -> Iterator[list[int]]:
    yield levels
    for i in range(len(levels)):
        yield levels[:i] + levels[i + 1 :]


def part_2(lines: list[str]):
    def is_safe(levels: list[int]) -> bool:
        increasing = None
        for i, (a, b) in enumerate(windowed(levels, 2)):
            if increasing is None:
                increasing = b > a

            if (increasing and a >= b) or (not increasing and b >= a) or abs(a - b) > 3:
                return False

        return True

    safe_sum = 0

    for line in lines:
        if any(is_safe(permutation) for permutation in permutations(ints(line))):
            safe_sum += 1

    return safe_sum


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
