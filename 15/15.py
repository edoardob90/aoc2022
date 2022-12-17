# pylint: disable=invalid-name,too-many-locals
"""AoC day 15, 2022: Beacon Exclusion Zone"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    patt = re.compile(r"-?\d+")
    sensors = {}
    for line in puzzle_input.splitlines():
        sx, sy, bx, by = map(int, patt.findall(line))
        sensors[(sx, sy)] = (bx, by)
    return sensors


def part1(data):
    """Solve part 1"""
    # Y = 10  # example input
    Y = 2_000_000
    known = set()
    cannot = set()
    for s, b in data.items():
        sx, sy = s
        bx, by = b
        distance = abs(sx - bx) + abs(sy - by)
        # (x, y) such that abs(sx - x) <= distance - abs(sy - y)
        offset = distance - abs(sy - Y)

        if offset < 0:
            continue

        lo_x, hi_x = sx - offset, sx + offset

        for x in range(lo_x, hi_x + 1):
            cannot.add(x)

        if by == Y:
            known.add(bx)

    return len(cannot - known)


def part1_faster(data):
    """Solve part 1 (with intervals)"""
    known = set()
    cannot = set()
    Y = 10  # example data
    # Y = 2_000_000
    intervals = []
    for s, b in data.items():
        sx, sy = s
        bx, by = b
        distance = abs(sx - bx) + abs(sy - by)
        # (x, y) such that abs(sx - x) <= distance - abs(sy - y)
        offset = distance - abs(sy - Y)

        if offset < 0:
            continue

        lo_x, hi_x = sx - offset, sx + offset
        intervals.append((lo_x, hi_x))

        if by == Y:
            known.add(by)

    intervals.sort()

    q = []

    for lo, hi in intervals:
        if not q:
            q.append([lo, hi])
            continue

        _, qhi = q[-1]

        if lo > qhi + 1:
            q.append([lo, hi])
            continue

        q[-1][1] = max(qhi, hi)

    # print(q)

    for lo, hi in q:
        for x in range(lo, hi + 1):
            cannot.add(x)

    return len(cannot - known)


def part2(data):
    """Solve part 2"""
    # M = 20 # example
    M = 4_000_000
    for Y in range(M + 1):

        intervals = []

        for s, b in data.items():
            sx, sy = s
            bx, by = b
            distance = abs(sx - bx) + abs(sy - by)

            # (x, y) such that abs(sx - x) <= distance - abs(sy - y)
            offset = distance - abs(sy - Y)

            if offset < 0:
                continue

            lo_x, hi_x = sx - offset, sx + offset
            intervals.append((lo_x, hi_x))

        intervals.sort()

        q = []

        for lo, hi in intervals:
            if not q:
                q.append([lo, hi])
                continue

            _, qhi = q[-1]

            if lo > qhi + 1:
                q.append([lo, hi])
                continue

            q[-1][1] = max(qhi, hi)

        # print(Y, q)

        # search for the disjoint intertval where the distress beacon lies
        x = 0
        for lo, hi in q:
            if x < lo:
                return x * 4_000_000 + Y

            x = max(x, hi + 1)

            if x > M:
                break


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    # solution1 = part1(data)
    solution1 = part1_faster(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
