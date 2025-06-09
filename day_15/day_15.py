from copy import deepcopy

from stdlib import *


def parse_input(lines: list[str]):
    warehouse_map = []
    while lines:
        line = lines.pop(0)
        if line.strip() == "":
            break
        warehouse_map.append(line)

    moves = ""
    for line in lines:
        moves += line.strip()

    return warehouse_map, moves


ARROWS = dict(zip("^>v<", DIRECTIONS))


def part_1(lines: list[str]):
    warehouse_map, moves = parse_input(lines)
    G = as_2d_graph(warehouse_map)
    dprint(graph_str(G))

    robot = Coord.from_tuple(
        one(n for n, d in G.nodes(data=True) if d.get("value") == "@")
    )

    for move in moves:
        direction = ARROWS[move]
        node = robot + direction
        value = G.nodes[node]["value"]
        if value == "#":
            continue
        elif value == ".":
            G.nodes[robot]["value"] = "."
            G.nodes[node]["value"] = "@"
            robot = node
        elif value == "O":
            # box
            nodes_to_move = [robot, node]
            while True:
                next_node = node + direction
                next_value = G.nodes[next_node]["value"]
                if next_value == ".":
                    # shift everything
                    for node_to_move in reversed(nodes_to_move):
                        G.nodes[node_to_move + direction]["value"] = G.nodes[
                            node_to_move
                        ]["value"]
                    G.nodes[robot]["value"] = "."
                    robot = robot + direction
                    break
                elif next_value == "#":
                    # wall
                    break
                elif next_value == "O":
                    nodes_to_move.append(next_node)
                    node = next_node

        dprint(graph_str(G))

    dprint(graph_str(G))
    boxes = [n for n, d in G.nodes(data=True) if d.get("value") == "O"]
    gps_sum = 0
    for x, y in boxes:
        gps_sum += x + 100 * y

    return gps_sum


def part_2(lines: list[str]):
    warehouse_map, moves = parse_input(lines)
    warehouse_map = [
        line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        for line in warehouse_map
    ]

    G = as_2d_graph(warehouse_map)
    dprint(graph_str(G))

    robot = Coord.from_tuple(
        one(n for n, d in G.nodes(data=True) if d.get("value") == "@")
    )

    for i, move in enumerate(moves):
        dprint(move, i)
        direction = ARROWS[move]
        node = robot + direction
        value = G.nodes[node]["value"]
        if value == "#":
            pass
        elif value == ".":
            G.nodes[robot]["value"] = "."
            G.nodes[node]["value"] = "@"
            robot = node
        elif value in "[]":
            # box
            nodes_to_move = [robot, node]

            heads = [node]
            if direction.y != 0:
                if value == "[":
                    right_bracket = node + Coord(1, 0)
                    assert G.nodes[right_bracket]["value"] == "]"
                    heads.append(right_bracket)
                    nodes_to_move.append(right_bracket)
                else:
                    left_bracket = node + Coord(-1, 0)
                    assert G.nodes[left_bracket]["value"] == "["
                    heads.append(left_bracket)
                    nodes_to_move.append(left_bracket)

            while True:
                hit_wall = False
                if all(G.nodes[head + direction]["value"] == "." for head in heads):
                    # shift everything
                    for node_to_move in unique_everseen(reversed(nodes_to_move)):
                        # swap ahead and behind
                        G.nodes[node_to_move + direction]["value"] = G.nodes[
                            node_to_move
                        ]["value"]
                        G.nodes[node_to_move]["value"] = "."
                    G.nodes[robot]["value"] = "."
                    robot = robot + direction
                    break

                # at least one head ran into a wall or another box
                next_heads = set()
                for head in heads:
                    next_node = head + direction
                    next_value = G.nodes[next_node]["value"]
                    if next_value == ".":
                        pass
                    elif next_value == "#":
                        # give up, can't move the boxes
                        hit_wall = True
                        break
                    elif next_value in "[]":
                        # add the box to heads
                        next_heads.add(next_node)
                        nodes_to_move.append(next_node)
                        if direction.y != 0:
                            if next_value == "[":
                                right_bracket = next_node + Coord(1, 0)
                                assert G.nodes[right_bracket]["value"] == "]"
                                next_heads.add(right_bracket)
                                nodes_to_move.append(right_bracket)
                            else:
                                left_bracket = next_node + Coord(-1, 0)
                                assert G.nodes[left_bracket]["value"] == "["
                                next_heads.add(left_bracket)
                                nodes_to_move.append(left_bracket)

                if hit_wall:
                    break

                heads = next_heads

        dprint(graph_str(G))

    dprint(graph_str(G))

    boxes = [n for n, d in G.nodes(data=True) if d.get("value") == "["]
    gps_sum = 0
    for x, y in boxes:
        gps_sum += x + 100 * y

    return gps_sum


if __name__ == "__main__":
    # DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(deepcopy(input_lines))))
    print("Part 2:", none_empty(part_2(deepcopy(input_lines))))
