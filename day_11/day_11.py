from functools import cache

from stdlib import *


@cache
def tick_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(stone_str := str(stone)) % 2 == 0:
        left = int(stone_str[: len(stone_str) // 2])
        right = int(stone_str[len(stone_str) // 2 :])
        return [left, right]
    else:
        return [stone * 2024]


def part_1(lines: list[str]):
    stones = Counter(ints(lines[0]))
    for j in range(25):
        next_stones = Counter()
        for v, c in stones.items():
            stone_counter = Counter(tick_stone(v))
            for nv in stone_counter.keys():
                stone_counter[nv] *= c
            next_stones.update(stone_counter)
        stones = next_stones

    return sum(stones.values())


def part_2(lines: list[str]):
    stones = Counter(ints(lines[0]))
    for j in range(75):
        next_stones = Counter()
        for v, c in stones.items():
            stone_counter = Counter(tick_stone(v))
            for nv in stone_counter.keys():
                stone_counter[nv] *= c
            next_stones.update(stone_counter)
        stones = next_stones

    return sum(stones.values())


if __name__ == "__main__":
    # DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
