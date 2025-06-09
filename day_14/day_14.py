from dataclasses import dataclass

from stdlib import *


@dataclass(eq=False)
class Robot:
    position: Coord
    velocity: Coord

    @classmethod
    def from_line(cls, line):
        nums = ints(line)
        return cls(Coord(nums[0], nums[1]), Coord(nums[2], nums[3]))

    def move(self):
        self.position = Coord(
            (self.position.x + self.velocity.x) % DIMS.x,
            (self.position.y + self.velocity.y) % DIMS.y,
        )


def tick(robots: list[Robot]):
    for robot in robots:
        robot.move()


def print_grid(robots: list[Robot]):
    def transform(g, c):
        v = g.get(c)
        return v if v != 0 else "."

    dprint(
        grid_str(
            Counter(robot.position for robot in robots),
            nx.grid_2d_graph(DIMS.x, DIMS.y, create_using=nx.Graph),
            transform=transform,
        )
    )


def robots_to_np_grid(robots: list[Robot]):
    grid = np.zeros((DIMS.y, DIMS.x))
    for pos, n in Counter(robot.position for robot in robots).items():
        grid[pos.y, pos.x] = 1

    return grid


def vertical_symmetry_score(grid):
    h, w = grid.shape
    half = w // 2
    left = grid[:, :half]
    right = np.fliplr(grid[:, -half:])  # handle even/odd width
    score = np.mean(left == right)
    return score


def part_1(lines: list[str]):
    robots = []
    for line in lines:
        robot = Robot.from_line(line)
        robots.append(robot)

    for _ in loops(100):
        tick(robots)

    print_grid(robots)

    quad_width = DIMS.x // 2
    quad_height = DIMS.y // 2

    q1 = [
        robot
        for robot in robots
        if robot.position.x < quad_width and robot.position.y < quad_height
    ]
    print_grid(q1)
    q2 = [
        robot
        for robot in robots
        if robot.position.x >= DIMS.x - quad_width and robot.position.y < quad_height
    ]
    print_grid(q2)
    q3 = [
        robot
        for robot in robots
        if robot.position.x < quad_width and robot.position.y >= DIMS.y - quad_height
    ]
    print_grid(q3)
    q4 = [
        robot
        for robot in robots
        if robot.position.x >= DIMS.x - quad_width
        and robot.position.y >= DIMS.y - quad_height
    ]
    print_grid(q4)

    return len(q1) * len(q2) * len(q3) * len(q4)


def part_2(lines: list[str]):
    robots = []
    for line in lines:
        robot = Robot.from_line(line)
        robots.append(robot)

    for i in count():
        tick(robots)
        v = vertical_symmetry_score(robots_to_np_grid(robots))
        if v > 0.97:
            print_grid(robots)
            return i + 1


if __name__ == "__main__":
    # DEBUG.true()
    # EXAMPLE.true()

    DIMS = Coord(101, 103)

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
