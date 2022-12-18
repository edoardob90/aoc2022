#!/usr/bin/env python
# pylint: disable=invalid-name,too-many-locals,unspecified-encoding
"""AoC day 18, 2022: Boiling Boulders"""

# Standard library imports
import pathlib
import sys
from collections import deque
from itertools import combinations

# Third party
# from codetiming import Timer


def parse(puzzle_input):
    """Parse input"""
    return [tuple(map(int, l.split(","))) for l in puzzle_input.splitlines()]


def euclid2(p1, p2):
    """Square of Euclidean distance in 3D"""
    x, y, z = p1
    X, Y, Z = p2
    return (x - X) ** 2 + (y - Y) ** 2 + (z - Z) ** 2


# @Timer(name="Part 1", text="{name}: {milliseconds:.3f} ms")
# ~81 ms
def part1(data):
    """Solve part 1"""
    count = 0
    for p1, p2 in combinations(data, 2):
        if euclid2(p1, p2) == 1:
            count += 1
    return 6 * len(data) - 2 * count


# @Timer(name="Part 2", text="{name}: {milliseconds:.3f} ms")
# ~220 ms
def part2(data):
    """Solve part 2"""
    droplet = set()  # our droplet's 1x1x1 cubes coordinates
    faces = {}  # keep track of how many times we see a face
    mx = my = mz = float("inf")  # min bounding box
    Mx = My = Mz = -float("inf")  # max bounding box

    offsets = [
        (0.5, 0, 0),
        (0, 0.5, 0),
        (0, 0, 0.5),
        (-0.5, 0, 0),
        (0, -0.5, 0),
        (0, 0, -0.5),
    ]

    for cell in data:
        x, y, z = cell
        droplet.add(cell)

        mx = min(mx, x)
        my = min(my, y)
        mz = min(mz, z)

        Mx = max(Mx, x)
        My = max(My, y)
        Mz = max(Mz, z)

        for dx, dy, dz in offsets:
            k = (x + dx, y + dy, z + dz)
            if k not in faces:
                faces[k] = 0
            faces[k] += 1

    # up to now is just Part 1 solution

    # we need to expand the bounding box by 1 in each dimension
    # to avoid starting our path-finding *inside* the first cube
    # and to make sure we explore all the empty space
    mx -= 1
    my -= 1
    mz -= 1

    Mx += 1
    My += 1
    Mz += 1

    path = deque([(mx, my, mz)])
    air = {(mx, my, mz)}

    while path:
        x, y, z = path.popleft()

        for dx, dy, dz in offsets:
            nx, ny, nz = k = (x + dx * 2, y + dy * 2, z + dz * 2)

            if not (mx <= nx <= Mx and my <= ny <= My and mz <= nz <= Mz):
                continue

            if k in droplet or k in air:
                continue

            air.add(k)
            path.append(k)

    free = set()

    for x, y, z in air:
        for dx, dy, dz in offsets:
            free.add((x + dx, y + dy, z + dz))

    return len(set(faces) & free)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
