#!/usr/bin/env python
# pylint: disable=invalid-name,too-many-locals,unspecified-encoding
"""AoC day 23, 2022: Unstable Diffusion"""

## Standard library imports
import pathlib
import sys

# import collections
# import functools
# import itertools

## Third-party
# from codetiming import Timer

# directions
DIRS = [-1j, 1j, -1, 1]  # N, S, W, E

# neighbors
NEIGH = DIRS + [-1 - 1j, 1 - 1j, -1 + 1j, 1 + 1j]

# attempted moves
ATTEMPTS = {
    -1j: (-1j - 1, -1j, -1j + 1),  # NW, N, NE
    1j: (1j - 1, 1j, 1j + 1),  # SW, S, SE
    1: (1 - 1j, 1, 1 + 1j),  # NE, E, SE
    -1: (-1 - 1j, -1, -1 + 1j),  # NW, W, SW
}


def parse_data(puzzle_input):
    """Parse input"""
    elves = set()
    for r, row in enumerate(puzzle_input.splitlines()):
        for c, col in enumerate(row.strip()):
            if col == "#":
                elves.add(c + r * 1j)
    return elves


# @Timer(name="Part 1", text="{name}: {milliseconds:.1f} ms")
def part1(elves):
    """Solve part 1"""
    for _ in range(10):
        # print(f"=== Round #{r} ===")
        once = set()
        twice = set()

        for elf in elves:
            if all(elf + x not in elves for x in NEIGH):
                continue

            for move in DIRS:
                if all(elf + x not in elves for x in ATTEMPTS[move]):
                    proposed = elf + move
                    if proposed in twice:
                        pass
                    elif proposed in once:
                        twice.add(proposed)
                    else:
                        once.add(proposed)
                    break

        # we must copy otherwise the iterable will change during iteration
        _elves = set(elves)

        for elf in _elves:
            if all(elf + x not in _elves for x in NEIGH):
                continue

            for move in DIRS:
                if all(elf + x not in _elves for x in ATTEMPTS[move]):
                    proposed = elf + move
                    if proposed not in twice:
                        elves.remove(elf)
                        elves.add(proposed)
                    break

        DIRS.append(DIRS.pop(0))

    # bounding box
    mx = min(x.real for x in elves)
    Mx = max(x.real for x in elves)
    my = min(x.imag for x in elves)
    My = max(x.imag for x in elves)

    return (Mx - mx + 1) * (My - my + 1) - len(elves)


# @Timer(name="Part 2", text="{name}: {milliseconds:.1f} ms")
def part2(elves):
    """Solve part 2"""
    last = set(elves)
    step = 1
    while True:
        # print(f"=== Round #{r} ===")
        once = set()
        twice = set()

        for elf in elves:
            if all(elf + x not in elves for x in NEIGH):
                continue

            for move in DIRS:
                if all(elf + x not in elves for x in ATTEMPTS[move]):
                    proposed = elf + move
                    if proposed in twice:
                        pass
                    elif proposed in once:
                        twice.add(proposed)
                    else:
                        once.add(proposed)
                    break

        # we must copy otherwise the iterable will change during iteration
        _elves = set(elves)

        for elf in _elves:
            if all(elf + x not in _elves for x in NEIGH):
                continue

            for move in DIRS:
                if all(elf + x not in _elves for x in ATTEMPTS[move]):
                    proposed = elf + move
                    if proposed not in twice:
                        elves.remove(elf)
                        elves.add(proposed)
                    break

        DIRS.append(DIRS.pop(0))

        if last == elves:
            break

        last = set(elves)
        step += 1

    return step


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    yield part1(parse_data(puzzle_input))
    yield part2(parse_data(puzzle_input))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
