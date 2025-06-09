import operator

from stdlib import *


def concat(left, right):
    return int(str(left) + str(right))


def calc(line, ops):
    target, initial, *rest = ints(line)
    for operators in product(ops, repeat=len(rest)):
        operations = zip(rest, operators)
        value = reduce(evaluate, operations, initial)
        if value == target:
            return value

    return 0


def evaluate(acc, elem):
    val, op = elem
    return op(acc, val)


def part_1(lines: list[str]):
    calibration_sum = 0
    for line in lines:
        calibration_sum += calc(line, [operator.add, operator.mul])

    return calibration_sum


def part_2(lines: list[str]):
    calibration_sum = 0
    for line in lines:
        calibration_sum += calc(line, [operator.add, operator.mul, concat])

    return calibration_sum


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
