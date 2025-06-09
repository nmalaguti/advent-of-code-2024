from stdlib import *
import heapq


def part_1(lines: list[str]):
    left = []
    right = []

    for line in lines:
        a, b = ints(line)
        heapq.heappush(left, a)
        heapq.heappush(right, b)

    sum_diff = 0

    for _ in range(len(left)):
        sum_diff += abs(heapq.heappop(right) - heapq.heappop(left))

    return sum_diff


def part_2(lines: list[str]):
    left = []
    right_counter = Counter()

    for line in lines:
        a, b = ints(line)
        left.append(a)
        right_counter[b] += 1

    sim_sum = 0

    for l in left:
        sim_sum += l * right_counter[l]

    return sim_sum


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
