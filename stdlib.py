import fileinput
import operator
import re
from collections import *
from collections.abc import Generator
from contextlib import ExitStack, contextmanager
from functools import cache, partial, reduce
from itertools import *
from pprint import pformat, pprint
from time import perf_counter
from typing import Callable, Iterator, NamedTuple, cast

import networkx as nx
import numpy as np
from anytree import Node, RenderTree
from funcy import rcompose
from more_itertools import *
from scipy.spatial.distance import cityblock


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    @classmethod
    def from_tuple(cls, tup):
        return Coord(tup[0], tup[1])

    @staticmethod
    def add(u, v):
        return tuple(np.add(u, v))

    @staticmethod
    def distance(u, v):
        return cityblock(u, v)

    @staticmethod
    def direction(u, v):
        return cast(tuple[int, int], tuple(np.subtract(v, u)))


DIRECTIONS = [
    Coord(0, -1),  # Up
    Coord(1, 0),  # Right
    Coord(0, 1),  # Down
    Coord(-1, 0),  # Left
]
UP, RIGHT, DOWN, LEFT = DIRECTIONS


class Flag:
    def __init__(self, flag: bool):
        self.flag = flag

    def true(self):
        self.flag = True

    def false(self):
        self.flag = False

    def __bool__(self):
        return self.flag


DEBUG = Flag(False)
EXAMPLE = Flag(False)

inf = float("inf")


def debug(*args):
    if DEBUG:
        if len(args) == 1:
            pprint(args[0])
        else:
            pprint(args)


def ints(line):
    return [int(x) for x in re.findall(r"-?\d+", line)]


def positive_ints(line):
    return [int(x) for x in re.findall(r"\d+", line)]


def read_input(filename=None):
    if filename is None:
        if EXAMPLE:
            filename = "example"
        else:
            filename = "input"

    return list(line.rstrip("\n") for line in fileinput.input(filename))


def identity(x):
    return x


def inverse_identity(x):
    return not x


def none_empty(x):
    return x if x is not None else ""


def as_grid(lines: list[str], *, transform=identity):
    grid = defaultdict()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            grid[(x, y)] = transform(c)

    return grid


def grid_str(*grids, transform=lambda g, c: g.get(c), max_x=inf, max_y=inf):
    grid = ChainMap(*grids)
    x = 0
    y = 0

    output = ""

    while True:
        cell = transform(grid, (x, y))
        if cell is None or x >= max_x or y >= max_y:
            if x == 0:
                break
            output += "\n"
            x = 0
            y = y + 1
        else:
            output += str(cell)
            x = x + 1

    return output


def grid_lines(lines: list[str]) -> Iterator[tuple[Coord, str]]:
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            yield Coord(x, y), c


def as_2d_graph(
    lines: list[str], *, transform=lambda v: dict(value=v), create_using=nx.DiGraph
) -> nx.Graph:
    width = len(lines[0])
    height = len(lines)

    G = nx.grid_2d_graph(width, height, create_using=create_using)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            G.nodes[(x, y)].update(transform(c))

    return G


def graph_index(G: nx.Graph) -> dict[str, list[Coord]]:
    index = defaultdict(list)
    for node, data in G.nodes(data=True):
        index[data["value"]].append(node)
    return index


def graph_str(G: nx.Graph, *, transform=operator.itemgetter("value")):
    output = ""

    min_x, max_x = minmax(x for (x, y) in G.nodes)
    min_y, max_y = minmax(y for (x, y) in G.nodes)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            output += transform(G.nodes.get((x, y)))
        output += "\n"

    return output


def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def dpprint(*args, **kwargs):
    if DEBUG:
        pprint(*args, **kwargs)


class timeit:
    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, type, value, traceback):
        self.time = perf_counter() - self.start
        self.readout = f"Time: {self.time:.6f} seconds"
        dprint(self.readout)


@contextmanager
def deferrer():
    with ExitStack() as es:
        yield es.callback


def visualize_graph(G: nx.DiGraph, root, key=None):
    nodes = {root: Node(str(root))}
    stack = [root]

    while stack:
        parent = stack.pop()
        for child in G.predecessors(parent):
            child_node = Node(str(child), parent=nodes[parent])
            nodes[child] = child_node
            stack.append(child)

    for pre, fill, node in RenderTree(nodes[root]):
        if key is not None:
            if callable(key):
                value = key(G, node.name)
            else:
                value = G.nodes[node.name].get(key)

            if value is None:
                dprint(f"{pre}{node.name}")
            else:
                dprint(f"{pre}{node.name} ({value})")
        else:
            dprint(f"{pre}{node.name}")


class _UniversalSet(set):
    def __and__(self, other):
        return other

    def __rand__(self, other):
        return other

    def __contains__(self, item):
        return True  # Optional: acts like it contains everything

    def __repr__(self):
        return "UniversalSet()"


UniversalSet = _UniversalSet()
