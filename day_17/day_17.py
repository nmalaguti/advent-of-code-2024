import pyximport
from stdlib import *

pyximport.install(
    language_level=3,
    setup_args={"include_dirs": [np.get_include()]},
)

# from interp import device
from device_optimized import device


def part_1(lines: list[str]):
    A = ints(lines[0])[0]
    B = ints(lines[1])[0]
    C = ints(lines[2])[0]
    assert not lines[3]
    program = np.array(ints(lines[4]), dtype=np.uint64)
    output = device(A, B, C, program)
    return ",".join(map(str, output))


def next_number(program: list[int], a, i):
    if i == len(program):
        print(a)
        exit()

    a2 = a << 3
    for b in range(8):
        if (b ^ (a2 + b >> (b ^ 7))) % 8 == program[i]:
            next_number(program, a2 + b, i + 1)


def part_2(lines: list[str]):
    program = np.array(ints(lines[4]), dtype=np.uint64)
    A = 0
    for i in reversed(range(len(program))):
        A <<= 3
        while not tuple(program[i:]) == tuple(device(A, 0, 0, program)):
            A += 1

    return A


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    with timeit():
        print("Part 1:", none_empty(part_1(input_lines)))
    with timeit():
        print("Part 2:", none_empty(part_2(input_lines)))
