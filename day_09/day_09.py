from sortedcontainers import SortedDict
from stdlib import *


@dataclass(eq=False)
class File:
    file_id: str
    file_length: int

    @property
    def is_empty(self):
        return self.file_id == "."


def EmptyFile(i: int):
    return File(".", i)


class Disk:
    def __init__(self):
        self.disk = deque()
        self.file_id_to_disk_index = {}
        self.empty_files = SortedDict()

    def append(self, file):
        self.disk.append(file)
        if not file.is_empty:
            self.file_id_to_disk_index[file.file_id] = len(self.disk) - 1
        else:
            self.empty_files.setdefault(file.file_length, deque()).append(
                (len(self.disk) - 1, file)
            )

    def __str__(self):
        output = []
        for f in self.disk:
            output.extend([f.file_id] * f.file_length)
        return "".join(output)

    def __len__(self):
        return len(self.disk)

    def __getitem__(self, i):
        return self.disk[i]

    def move(self, file_id, i):
        file_index = self.file_id_to_disk_index[file_id]
        file = self.disk[file_index]

        self.disk[file_index] = EmptyFile(file.file_length)

        while file_index - 1 >= 0 and self.disk[file_index - 1].is_empty:
            file_index -= 1

        while file_index + 1 < len(self.disk) and self.disk[file_index + 1].is_empty:
            self.disk[file_index].file_length += self.disk[file_index + 1].file_length
            del self.disk[file_index + 1]

        empty_file = self.disk[i]
        assert empty_file.is_empty

        self.disk.insert(i, file)
        empty_file.file_length -= file.file_length
        if empty_file.file_length == 0:
            del self.disk[i + 1]

        # update index
        for j in range(i, len(self.disk)):
            if not self.disk[j].is_empty:
                self.file_id_to_disk_index[self.disk[j].file_id] = j

        self.empty_files = SortedDict()
        for i, f in enumerate(self.disk):
            if f.is_empty:
                self.empty_files.setdefault(f.file_length, deque()).append((i, f))

    def find_empty(self, file):
        max_value = self.file_id_to_disk_index[file.file_id]
        first_empty = None

        for key in self.empty_files.irange(file.file_length):
            index = self.empty_files[key][0][0]
            if index > max_value:
                continue

            if first_empty is None or index < first_empty:
                first_empty = index

        return first_empty


def part_1(lines: list[str]):
    line = lines[0]
    files = {}
    output = deque()
    if len(line) % 2 != 0:
        line += "0"

    for i, (flen, empty_len) in enumerate(batched(line, n=2)):
        files[i] = int(flen)
        output.extend([str(i)] * int(flen))
        output.extend(["."] * int(empty_len))

    i = 0
    while i < len(output):
        if output[i] == ".":
            while (final := output.pop()) == ".":
                continue
            output[i] = final
        i += 1

    checksum = 0
    for i, fid in enumerate(output):
        checksum += i * int(fid)

    return checksum


def part_2(lines: list[str]):
    line = lines[0]
    files = {}
    if len(line) % 2 != 0:
        line += "0"

    disk = Disk()
    for i, (flen, empty_len) in enumerate(batched(line, n=2)):
        f = File(str(i), int(flen))
        files[str(i)] = f
        disk.append(f)
        if int(empty_len) > 0:
            disk.append(EmptyFile(int(empty_len)))

    last_file_id = i
    while last_file_id >= 0:
        last_file = files[str(last_file_id)]
        index = disk.find_empty(last_file)
        if index is not None:
            disk.move(str(last_file_id), index)

        last_file_id -= 1

    i = 0
    checksum = 0
    for f in disk.disk:
        if f.is_empty:
            i += f.file_length
            continue

        for _ in range(f.file_length):
            checksum += i * int(f.file_id)
            i += 1

    dprint(disk)

    return checksum


if __name__ == "__main__":
    DEBUG.true()
    EXAMPLE.true()

    input_lines = read_input()
    print("Part 1:", none_empty(part_1(input_lines)))
    print("Part 2:", none_empty(part_2(input_lines)))
