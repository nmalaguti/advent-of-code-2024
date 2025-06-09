from dataclasses import dataclass

from stdlib import *


@dataclass(frozen=True)
class Region:
    letter: str
    nodes: set[tuple[int, int]]
    graph: nx.Graph

    def __iter__(self):
        return iter(self.nodes)

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, coord):
        return coord in self.nodes

    @property
    def perimeter(self) -> int:
        perimeter = 0

        for x, y in self:
            for dx, dy in DIRECTIONS:
                neighbor = x + dx, y + dy
                if neighbor not in self:
                    perimeter += 1

        return perimeter

    @property
    def area(self) -> int:
        return len(self)

    @property
    def sides(self) -> int:
        # number of sides == number of vertices
        # each node has 4 potential vertices
        # a convex vertex is when the edge of a node doesn't connect to the region on 2 adjacent sides
        # a concave vertex is when a node has 2 adjacent edges in the region and the diagonal node is not
        total_vertices = 0

        for node in self:
            convex_vertices = 0
            concave_vertices = 0

            x, y = node
            adjacent_sides = map(partial(take, 2), circular_shifts(DIRECTIONS))
            for (dx1, dy1), (dx2, dy2) in adjacent_sides:
                neigh1, neigh2 = (x + dx1, y + dy1), (x + dx2, y + dy2)
                diag = (x + dx1 + dx2, y + dy1 + dy2)
                if neigh1 not in self and neigh2 not in self:
                    convex_vertices += 1
                elif neigh1 in self and neigh2 in self and diag not in self:
                    concave_vertices += 1

            total_vertices += convex_vertices + concave_vertices

        return total_vertices


def split_by_value_regions(G, attr="value") -> list[Region]:
    undirected = G.to_undirected()

    regions: list[Region] = []

    values = set(nx.get_node_attributes(G, attr).values())
    for v in values:
        # Filter nodes with the same value
        nodes = [n for n, d in G.nodes(data=True) if d[attr] == v]
        sub = undirected.subgraph(nodes)
        r = [
            Region(letter=v, nodes=set(comps), graph=G)
            for comps in nx.connected_components(sub)
        ]
        regions.extend(r)

    return regions


def part_1(lines: list[str]):
    G = as_2d_graph(lines)
    regions = split_by_value_regions(G)
    return sum(region.area * region.perimeter for region in regions)


def part_2(lines: list[str]):
    G = as_2d_graph(lines).to_undirected()
    regions = split_by_value_regions(G)

    return sum(region.area * region.sides for region in regions)


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
