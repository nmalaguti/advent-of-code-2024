import operator

from stdlib import *


def part_1(lines: list[str]):
    grid = as_grid(lines)
    max_x = len(lines[0])
    max_y = len(lines)

    result = map_reduce(
        grid.items(), keyfunc=operator.itemgetter(1), valuefunc=operator.itemgetter(0)
    )
    result.pop(".")

    antinodes = defaultdict()

    for freq, locs in result.items():
        for (a_x, a_y), (b_x, b_y) in permutations(locs, 2):
            x_slope = a_x - b_x
            y_slope = a_y - b_y
            antinode_x = b_x - x_slope
            antinode_y = b_y - y_slope
            if 0 <= antinode_x < max_x and 0 <= antinode_y < max_y:
                antinodes[(antinode_x, antinode_y)] = "#"

    if DEBUG:
        print(grid_str(antinodes, grid))

    return len(antinodes)


def part_2(lines: list[str]):
    grid = as_grid(lines)
    max_x = len(lines[0])
    max_y = len(lines)

    result = map_reduce(
        grid.items(), keyfunc=operator.itemgetter(1), valuefunc=operator.itemgetter(0)
    )
    result.pop(".")

    antinodes = defaultdict()

    for freq, locs in result.items():
        for loc in locs:
            antinodes[loc] = "#"

        for (a_x, a_y), (b_x, b_y) in permutations(locs, 2):
            x_slope = a_x - b_x
            y_slope = a_y - b_y
            antinode_x = b_x - x_slope
            antinode_y = b_y - y_slope
            while 0 <= antinode_x < max_x and 0 <= antinode_y < max_y:
                antinodes[(antinode_x, antinode_y)] = "#"
                antinode_x -= x_slope
                antinode_y -= y_slope

    if DEBUG:
        print(grid_str(antinodes, grid))

    return len(antinodes)


if __name__ == "__main__":
    # DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
