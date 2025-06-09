from stdlib import *


def part_1(lines: list[str]):
    G = nx.Graph()
    for line in lines:
        u, v = line.split("-")
        G.add_edge(u, v)

    cliques_with_t = list(
        clique
        for clique in nx.enumerate_all_cliques(G)
        if len(clique) == 3 and any(node.startswith("t") for node in clique)
    )

    return len(cliques_with_t)


def part_2(lines: list[str]):
    G = nx.Graph()
    for line in lines:
        u, v = line.split("-")
        G.add_edge(u, v)

    cliques = list(nx.find_cliques(G))
    max_len = max(len(c) for c in cliques)
    max_clique = one(c for c in cliques if len(c) == max_len)

    return ",".join(sorted(max_clique))


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
