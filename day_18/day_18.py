from stdlib import *


def part_1(lines: list[str]):
    G = nx.grid_2d_graph(DIMS.x, DIMS.y, create_using=nx.DiGraph)
    for line in lines[:1024]:
        x, y = ints(line)
        G.remove_node((x, y))

    return nx.shortest_path_length(G, (0, 0), (DIMS.x - 1, DIMS.y - 1))


def part_2(lines: list[str]):
    G = nx.grid_2d_graph(DIMS.x, DIMS.y, create_using=nx.DiGraph)
    for i, line in enumerate(lines):
        x, y = ints(line)
        G.remove_node((x, y))
        if i >= 1024:
            try:
                nx.shortest_path_length(G, (0, 0), (DIMS.x - 1, DIMS.y - 1))
            except nx.NetworkXNoPath:
                return f"{x},{y}"

    return None


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    DIMS = Coord(71, 71)

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
