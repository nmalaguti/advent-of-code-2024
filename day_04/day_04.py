from typing import Iterator

from stdlib import *


def offsets(x, y, offs) -> Iterator[tuple[int, int]]:
    for xo, yo in offs:
        yield x + xo, y + yo


def part1_orientations(x, y) -> Iterator[list[tuple[int, int]]]:
    zeros = list(repeat(0, 4))
    increasing = list(range(4))
    decreasing = list(map(lambda x: 0 - x, increasing))

    yield list(offsets(x, y, zip(increasing, zeros)))  # EE
    yield list(offsets(x, y, zip(decreasing, zeros)))  # WW
    yield list(offsets(x, y, zip(zeros, increasing)))  # SS
    yield list(offsets(x, y, zip(zeros, decreasing)))  # NN

    yield list(offsets(x, y, zip(increasing, decreasing)))  # NE
    yield list(offsets(x, y, zip(decreasing, decreasing)))  # NW
    yield list(offsets(x, y, zip(increasing, increasing)))  # SE
    yield list(offsets(x, y, zip(decreasing, increasing)))  # SW


def part2_orientations(x, y) -> Iterator[list[tuple[int, int]]]:
    yield [(x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]


def word(grid: dict[tuple[int, int], str], coords: list[tuple[int, int]]) -> str | None:
    char_list = []
    for x, y in coords:
        c = grid.get((x, y))
        if c is None:
            return None
        char_list.append(c)
    return "".join(char_list)


def part_1(lines: list[str]):
    grid = as_grid(lines)

    xmas_sum = 0
    for (x, y), c in grid.items():
        if c == "X":
            for offs in part1_orientations(x, y):
                letters = word(grid, offs)
                if letters == "XMAS":
                    xmas_sum += 1

    return xmas_sum


def part_2(lines: list[str]):
    grid = as_grid(lines)

    xmas_sum = 0
    for (x, y), c in grid.items():
        if c == "A":
            for offs in part2_orientations(x, y):
                letters = word(grid, offs)
                if letters in ["MMSS", "MSMS", "SSMM", "SMSM"]:
                    xmas_sum += 1

    return xmas_sum


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
