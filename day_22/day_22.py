from numba import njit, types
from stdlib import *


@njit(inline="always", cache=True)
def mix(a: int, b: int) -> int:
    return a ^ b


@njit(inline="always", cache=True)
def prune(x: int) -> int:
    return x & 0xFFFFFF


@njit(cache=True)
def pseudorandom(secret: int, steps: int):
    result = np.zeros(steps + 1, dtype=np.int64)
    result[0] = secret
    s = secret
    for i in range(steps):
        s = prune(mix(s, s << 6))
        s = prune(mix(s, s >> 5))
        s = prune(mix(s, s << 11))

        result[i + 1] = s
    return result


pseudorandom.compile((types.long_, types.long_))


def part_1(lines: list[str]):
    total = 0
    for line in lines:
        secret = ints(line)[0]
        result = pseudorandom(secret, 2000)
        total += result[-1]
    return total


def part_2(lines: list[str]):
    lookup = defaultdict(int)
    for line in lines:
        seen = set()

        results = pseudorandom(ints(line)[0], 2000)
        ones_digits = results % 10
        deltas = ones_digits[1:] - ones_digits[:-1]

        for result, window in zip(ones_digits[4:], windowed(deltas, 4)):
            if window not in seen:
                seen.add(window)
                lookup[window] += result

    return max(lookup.values())


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
