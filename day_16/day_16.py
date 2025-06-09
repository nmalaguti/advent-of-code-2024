from stdlib import *

CoordDir = tuple[Coord, Coord]


def build_directional_graph(lines: list[str], straight_cost=1, turn_cost=1000):
    width = len(lines[0])
    height = len(lines)

    G = nx.DiGraph()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                continue

            for dir_from in DIRECTIONS:
                coord = Coord(x, y)
                node = (coord, dir_from)
                G.add_node(node, value=c)

                # can't have edges from invalid nodes
                from_coord = coord + dir_from
                if not (0 <= from_coord.x < width and 0 <= from_coord.y < height):
                    continue

                for dir_to in DIRECTIONS:
                    to_coord = coord + dir_to
                    if not (0 <= to_coord.x < width and 0 <= to_coord.y < height):
                        continue

                    next_node = (to_coord, dir_to)

                    if dir_to == dir_from:
                        cost = straight_cost
                    else:
                        cost = turn_cost + straight_cost

                    G.add_edge(node, next_node, weight=cost)

    ends = list(node for node, data in G.nodes(data=True) if data.get("value") == "E")
    pointing_at_ends = set()
    for end in ends:
        pointing_at_ends |= set(G.predecessors(end))

    G.remove_nodes_from(ends)

    end_coord = first(ends)[0]
    end_node = (Coord.from_tuple(end_coord), Coord(0, 0))
    G.add_node(end_node, value="E")
    for node in pointing_at_ends:
        G.add_edge(node, end_node, weight=straight_cost)

    return G


def part_1(lines: list[str]):
    G = build_directional_graph(lines)

    start = one(
        node
        for node, data in G.nodes(data=True)
        if data.get("value") == "S" and node[1] == Coord(1, 0)
    )
    end = one(node for node, data in G.nodes(data=True) if data.get("value") == "E")
    cost = nx.shortest_path_length(G, start, end, weight="weight")

    return cost


def part_2(lines: list[str]):
    G = build_directional_graph(lines)

    start = one(
        node
        for node, data in G.nodes(data=True)
        if data.get("value") == "S" and node[1] == Coord(1, 0)
    )
    end = one(node for node, data in G.nodes(data=True) if data.get("value") == "E")

    paths = nx.all_shortest_paths(G, start, end, weight="weight")
    coords = set()
    for path in paths:
        for node in path:
            coords.add(node[0])

    return len(coords)


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
