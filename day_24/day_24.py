from typing import Iterable

from stdlib import *


def n_node(c: str, n: int) -> str:
    return f"{c}{n:02}"


def node_op(G: nx.DiGraph, node: str) -> str | None:
    edges = G.in_edges(node, data=True)
    if edges:
        u, v, d = first(edges)
        op = d["op"]
        return op.__name__.rstrip("_")
    return None


def subgraph_for_z(G: nx.DiGraph, n: int) -> nx.DiGraph:
    z_gate = get_z_gate(G, n) or n_node("z", n)

    unique_nodes = set(nx.ancestors(G, z_gate))
    if n > 0:
        prev_z_gate = get_z_gate(G, n - 1) or n_node("z", n - 1)
        unique_nodes -= set(nx.ancestors(G, prev_z_gate))

    all_nodes = set(collapse(G.out_edges(node) for node in unique_nodes))
    return G.subgraph(all_nodes).to_directed()


def visualize_subgraph(G: nx.DiGraph, n: int):
    subgraph = subgraph_for_z(G, n)
    z_gate = get_z_gate(G, n) or n_node("z", n)

    visualize_graph(subgraph, get_xy_and_gate(G, n), node_op)
    visualize_graph(subgraph, get_xy_xor_gate(G, n), node_op)
    visualize_graph(subgraph, z_gate, node_op)
    dprint("")


def evaluate(G, node):
    value = G.nodes[node].get("value")
    if value is not None:
        return value

    u, v = G.predecessors(node)

    u_value = evaluate(G, u)
    v_value = evaluate(G, v)
    edge = G.get_edge_data(u, node)
    op = edge["op"]

    return op(u_value, v_value)


def from_bits(wires: Iterable[int]) -> int:
    return sum(bit << i for i, bit in enumerate(z for z in wires))


def to_bits(num: int) -> list[int]:
    return [int(b) for b in reversed(bin(num)[2:])]


def set_nodes(G, prefix, value):
    bits = to_bits(value)
    # zero out values
    for i in range(G.graph[f"{prefix}s"]):
        bit = 0
        if i < len(bits):
            bit = bits[i]
        G.nodes[n_node(prefix, i)]["value"] = bit


def validate(G: nx.DiGraph, n: int) -> bool:
    for x, y, c in product(range(2), repeat=3):
        if n == 0 and c > 0:
            continue

        G_copy = G.copy(as_view=False)

        c_value = c << n - 1 if n > 0 else 0
        x_value = (x << n) + c_value
        y_value = (y << n) + c_value

        set_nodes(G_copy, "x", x_value)
        set_nodes(G_copy, "y", y_value)

        z_value = evaluate(G_copy, n_node("z", n))
        if z_value != (x + y + c) % 2:
            return False

    return True


def find_node_by_io(
    G: nx.DiGraph,
    *,
    in_nodes: set | None = None,
    out_nodes: set | None = None,
    in_op=None,
) -> str | None:
    if in_nodes is None:
        in_nodes = set()
    if out_nodes is None:
        out_nodes = set()

    candidates = set()

    for u, v, d in G.edges(data=True):
        if in_op is not None and d.get("op") != in_op:
            continue

        in_edges = set(G.predecessors(v))
        out_edges = set(G.successors(v))

        if in_nodes.issubset(in_edges) and out_nodes.issubset(out_edges):
            candidates.add(v)

    return first(candidates, None)


def get_xy_and_gate(G: nx.DiGraph, n: int) -> str | None:
    return find_node_by_io(
        G,
        in_nodes={n_node("x", n), n_node("y", n)},
        in_op=operator.and_,
    )


def get_xy_xor_gate(G: nx.DiGraph, n: int) -> str | None:
    return find_node_by_io(
        G,
        in_nodes={n_node("x", n), n_node("y", n)},
        in_op=operator.xor,
    )


def get_or_gate(G: nx.DiGraph, n: int) -> str | None:
    xy_and_gate = get_xy_and_gate(G, n - 1)
    return find_node_by_io(G, in_nodes={xy_and_gate}, in_op=operator.or_)


def get_z_gate(G: nx.DiGraph, n: int) -> str | None:
    or_gate = get_or_gate(G, n)
    xy_xor_gate = get_xy_xor_gate(G, n)
    return find_node_by_io(G, in_nodes={or_gate, xy_xor_gate}, in_op=operator.xor)


def swap_wires(G: nx.DiGraph, a, b):
    # Record in-edges with data
    a_in = list(G.in_edges(a, data=True))
    b_in = list(G.in_edges(b, data=True))

    # Remove existing in-edges
    for u, _, _ in a_in:
        G.remove_edge(u, a)
    for u, _, _ in b_in:
        G.remove_edge(u, b)

    # Add swapped edges
    for u, _, data in a_in:
        G.add_edge(u, b, **data)
    for u, _, data in b_in:
        G.add_edge(u, a, **data)


def fix_wires(G: nx.DiGraph, n: int):
    z_node = n_node("z", n)
    dprint(f"\nFOR NODE {z_node}\n")
    visualize_subgraph(G, n)

    xy_xor_gate = get_xy_xor_gate(G, n)
    or_gate = get_or_gate(G, n)
    z_gate = find_node_by_io(G, in_nodes={or_gate, xy_xor_gate}, in_op=operator.xor)
    if z_gate is None:
        z_gate = z_node
        to_swap = set(G.predecessors(z_gate)) ^ {xy_xor_gate, or_gate}
    elif z_gate != z_node:
        to_swap = {z_node, z_gate}
    else:
        raise RuntimeError("Expected switched wires but didn't find them")

    dprint(to_swap)
    swap_wires(G, *to_swap)

    dprint("FIXED")
    visualize_subgraph(G, n)

    return to_swap


def load_graph(lines: list[str]) -> nx.DiGraph:
    lines = deque(lines)
    values = []

    while lines and lines[0]:
        values.append(lines.popleft())

    if lines:
        lines.popleft()

    G = nx.DiGraph()
    for value in values:
        node, val = value.split(": ")
        G.add_node(node, value=int(val))

    for gate in lines:
        u, op, v, _, target = gate.split()
        if op == "XOR":
            op_func = operator.xor
        elif op == "AND":
            op_func = operator.and_
        elif op == "OR":
            op_func = operator.or_
        else:
            raise ValueError(f"Unknown operator {op}")

        G.add_edge(u, target, op=op_func)
        G.add_edge(v, target, op=op_func)

    for node in G.nodes:
        preds = list(G.predecessors(node))
        assert len(preds) == 0 or len(preds) == 2

    G.graph["xs"] = sum(1 for node in G.nodes if node.startswith("x"))
    G.graph["ys"] = sum(1 for node in G.nodes if node.startswith("y"))
    G.graph["zs"] = sum(1 for node in G.nodes if node.startswith("z"))

    return G


def part_1(lines: list[str]):
    G = load_graph(lines)
    return from_bits([evaluate(G, n_node("z", i)) for i in range(G.graph["zs"])])


def part_2(lines: list[str]):
    G = load_graph(lines)

    swaps = set()
    for i in range(G.graph["zs"] - 1):
        if not validate(G, i):
            swaps |= fix_wires(G, i)

    return ",".join(sorted(swaps))


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
