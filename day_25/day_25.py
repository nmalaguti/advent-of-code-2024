from stdlib import *


def part_1(lines: list[str]):
    locks = []
    keys = []
    for schematic in split_at(lines, lambda l: not l.strip()):
        is_lock = schematic[0] == "#####"
        arr = np.array([list(row) for row in schematic], dtype=str)
        if is_lock:
            heights = np.sum(arr[1:].T == "#", axis=1)
            locks.append(heights)
        else:
            heights = np.sum(arr[:-1].T == "#", axis=1)
            keys.append(heights)

    locks = np.array(locks, dtype=int)
    keys = np.array(keys, dtype=int)

    result = locks[:, None, :] + keys[None, :, :]
    mask = np.all(result <= 5, axis=2)

    return np.sum(mask)


def part_2(lines: list[str]):
    pass


if __name__ == "__main__":
    DEBUG.true()
    # EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
