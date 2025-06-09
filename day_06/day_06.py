from copy import deepcopy

from stdlib import *

UP = (0, -1)  # up
RIGHT = (1, 0)  # right
DOWN = (0, 1)  # down
LEFT = (-1, 0)  # left

directions = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}


class Directions:
    def __init__(self, current=UP):
        self.current = current

    @property
    def next(self):
        return directions[self.current]

    def turn(self):
        self.current = self.next


def advance(coord, direction):
    return tuple(map(sum, zip(coord, direction)))


def peek(grid, coord, direction):
    while True:
        next_coord = advance(coord, direction)
        cell = grid.get(next_coord)
        if cell is None:
            return cell
        if cell == "#":
            break
        coord = next_coord

    return grid.get(advance(coord, directions[direction])) == "X"


def loops(grid, coord, direction):
    visited_from = defaultdict(set)
    visited_to = defaultdict(set)

    def fancy_cell(grid, coord):
        dirs = visited_to.get(coord)
        val = grid.get(coord)
        if val == "^":
            return val

        if dirs is None:
            return val

        vert = any(z != 0 for (_, (_, z)) in dirs)
        horz = any(z != 0 for (_, (z, _)) in dirs)

        if vert and horz:
            return "+"
        elif vert:
            return "|"
        elif horz:
            return "-"
        else:
            return "?"

    turns = Directions(direction)
    last_turn = None
    while True:
        next_coord = advance(coord, turns.current)
        cell = grid.get(next_coord)

        if (coord, turns.current) in visited_from.get(next_coord, []):
            if DEBUG:
                print(grid_str(grid, transform=fancy_cell))

            return True

        if cell is None:
            return False

        visited_to[coord].add((next_coord, turns.current))

        if cell in ["#", "O"]:
            last_turn = cell
            turns.turn()
        else:
            visited_from[next_coord].add((coord, turns.current))
            coord = next_coord


def part_1(lines: list[str]):
    grid = as_grid(lines)
    reverse_lookup = defaultdict(set)

    for (x, y), c in grid.items():
        reverse_lookup[c].add((x, y))

    coord = first(reverse_lookup["^"])

    turns = cycle(directions)
    direction = next(turns)

    while True:
        grid[coord] = "X"
        next_coord = advance(coord, direction)
        val = grid.get(next_coord)
        if val is None:
            break

        if val == "#":
            # turn right
            direction = next(turns)
        else:
            coord = next_coord

    return sum(1 for c in grid.values() if c == "X")


def part_2(lines: list[str]):
    grid = as_grid(lines)
    reverse_lookup = defaultdict(set)

    for (x, y), c in grid.items():
        reverse_lookup[c].add((x, y))

    coord = first(reverse_lookup["^"])

    turns = Directions()
    visited_from = defaultdict(set)
    steps = 0

    while True:
        next_coord = advance(coord, turns.current)
        cell = grid.get(next_coord)
        if cell is None:
            break

        if cell == "#":
            turns.turn()
        else:
            steps += 1
            visited_from[next_coord].add((coord, turns.current, steps))
            coord = next_coord

    obstacle_options = set()

    for coord, froms in visited_from.items():
        sorted_froms = sorted(froms, key=lambda x: x[-1])
        for prev_coord, direction, distance in sorted_froms:
            assert direction == tuple(
                map(lambda a: a[0] - a[1], zip(coord, prev_coord))
            )

            if loops(ChainMap({coord: "O"}, grid), prev_coord, direction):
                obstacle_options.add(coord)
            else:
                break

    return len(obstacle_options)


if __name__ == "__main__":
    # DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
