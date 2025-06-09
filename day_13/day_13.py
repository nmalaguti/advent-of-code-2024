import operator
from dataclasses import dataclass

from stdlib import *
from z3 import *


@dataclass
class Machine:
    prize: Coord
    button_a: Coord
    button_b: Coord


def optimal(machine: Machine):
    A = Int("A")
    B = Int("B")

    opt = Optimize()
    opt.add(machine.button_a.x * A + machine.button_b.x * B == machine.prize.x)
    opt.add(machine.button_a.y * A + machine.button_b.y * B == machine.prize.y)
    opt.add(A >= 0, B >= 0)

    C = 3 * A + B
    opt.minimize(C)

    if opt.check() == sat:
        model = opt.model()
        return model.eval(C).as_long()
    else:
        return 0


def part_1(lines: list[str]):
    machines = []
    for button_a, button_b, prize, *rest in chunked(lines, 4):
        machines.append(
            Machine(Coord(*ints(prize)), Coord(*ints(button_a)), Coord(*ints(button_b)))
        )

    total_tokens = 0
    for machine in machines:
        total_tokens += optimal(machine)

    return total_tokens


def part_2(lines: list[str]):
    machines = []
    for button_a, button_b, prize, *rest in chunked(lines, 4):
        machines.append(
            Machine(
                Coord(*map(partial(operator.add, 10000000000000), ints(prize))),
                Coord(*ints(button_a)),
                Coord(*ints(button_b)),
            )
        )

    total_tokens = 0
    for machine in machines:
        total_tokens += optimal(machine)

    return total_tokens


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
