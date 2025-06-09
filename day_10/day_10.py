from stdlib import *


def part_1(lines: list[str]):
    G = as_2d_graph(lines, transform=lambda v: dict(height=int(v)))

    for u, v in list(G.edges):
        h1 = G.nodes[u]["height"]
        h2 = G.nodes[v]["height"]
        if h2 != h1 + 1:
            G.remove_edge(u, v)

    dprint(graph_str(G, transform=lambda v: str(v.get("height", "?"))))

    trailhead_sum = 0

    for node in G.nodes:
        if G.nodes[node]["height"] == 0:
            reachable = nx.descendants(G, node)
            trailhead_sum += sum(1 for n in reachable if G.nodes[n]["height"] == 9)

    return trailhead_sum


def part_2(lines: list[str]):
    G = as_2d_graph(lines, transform=lambda v: dict(height=int(v)))

    for u, v in list(G.edges):
        h1 = G.nodes[u]["height"]
        h2 = G.nodes[v]["height"]
        if h2 != h1 + 1:
            G.remove_edge(u, v)

    dprint(graph_str(G, transform=lambda v: str(v.get("height", "?"))))

    trailhead_sum = 0

    for start in G.nodes:
        if G.nodes[start]["height"] != 0:
            continue

        reachable = nx.descendants(G, start)
        targets = [n for n in reachable if G.nodes[n]["height"] == 9]

        for target in targets:
            paths = list(nx.all_simple_paths(G, start, target))
            trailhead_sum += len(paths)

    return trailhead_sum


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
