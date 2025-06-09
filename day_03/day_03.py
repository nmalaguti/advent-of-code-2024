from stdlib import *


def part_1(lines: list[str]):
    line = "".join(lines)
    mul_sum = 0
    for mul in re.findall(r"mul\(\d{1,3},\d{1,3}\)", line):
        a, b = ints(mul)
        mul_sum += a * b

    return mul_sum


def part_2(lines: list[str]):
    line = "".join(lines)
    mul_sum = 0
    enabled = True
    for instruction in re.findall(r"(mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))", line):
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        elif enabled:
            a, b = ints(instruction)
            mul_sum += a * b

    return mul_sum


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
