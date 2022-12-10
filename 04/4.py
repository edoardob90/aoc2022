# pylint: disable=invalid-name
"""AoC day 4, 2022"""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """Parse input"""
    data = [
        list(map(lambda p: list(map(int, p.split("-"))), pair.split(",")))
        for pair in puzzle_input.splitlines()
    ]
    # build a list of pairs of sets
    sets = []
    for p1, p2 in data:
        # range must be inclusive
        p1[1] += 1
        p2[1] += 1
        p1, p2 = map(lambda x: set(range(*x)), (p1, p2))
        sets.append((p1, p2))

    return sets


def part1(data):
    """Solve part 1"""
    overlaps = 0
    for p1, p2 in data:
        if p1 <= p2 or p1 >= p2:
            overlaps += 1

    return overlaps


def part2(data):
    """Solve part 2"""
    overlaps = 0
    for p1, p2 in data:
        if p1 & p2:
            overlaps += 1

    return overlaps


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
