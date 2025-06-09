from stdlib import *


def manhattan_distance(u: tuple[int, int], v: tuple[int, int]):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])


def get_path(G, start):
    path = {}
    location = start
    visited = set()
    i = 0
    while True:
        path[i] = location
        G.nodes[location]["order"] = i
        visited.add(location)
        for neighbor in G.neighbors(location):
            if G.nodes[neighbor]["value"] in "SE." and neighbor not in visited:
                location = neighbor
                i += 1
                break
        else:
            break

    return path


def part_1(lines: list[str]):
    G = as_2d_graph(lines, create_using=nx.Graph)
    index = graph_index(G)

    start = one(index["S"])
    ordered_path = get_path(G, start)

    cheats = set()
    counter = Counter()
    for i in range(len(ordered_path)):
        coord = ordered_path[i]
        coord_node = G.nodes[coord]
        for wall in G.neighbors(coord):
            wall_node = G.nodes[wall]
            if wall_node["value"] == "#":
                for cheat_to in G.neighbors(wall):
                    if cheat_to == coord:
                        continue
                    cheat_node = G.nodes[cheat_to]
                    if cheat_node["value"] in "SE.":
                        pico_saved = (
                            cheat_node["order"]
                            - coord_node["order"]
                            - 2  # cost to traverse the wall
                        )
                        if pico_saved >= 100:
                            cheats.add((coord, cheat_to))
                            counter[pico_saved] += 1

    return len(cheats)


def part_2(lines: list[str]):
    G = as_2d_graph(lines, create_using=nx.Graph)
    index = graph_index(G)

    start = one(index["S"])
    ordered_path = get_path(G, start)

    cheats = set()
    counter = Counter()
    for i in range(len(ordered_path)):
        coord = ordered_path[i]
        coord_node = G.nodes[coord]
        for cheat_coord in ordered_path.values():
            if cheat_coord == coord:
                continue
            distance = manhattan_distance(coord, cheat_coord)
            if distance > 20:
                continue
            cheat_node = G.nodes[cheat_coord]
            pico_saved = cheat_node["order"] - coord_node["order"] - distance
            if pico_saved >= 100:
                cheats.add((coord, cheat_coord))
                counter[pico_saved] += 1

    return len(cheats)


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
