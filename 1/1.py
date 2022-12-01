# pylint: disable=invalid-name
"""AoC day 1, 2022"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    lines = [
        list(map(int, line.strip().split("\n")))
        for line in re.split(r"^$", puzzle_input, flags=re.M)
    ]
    return sorted([sum(l) for l in lines], reverse=True)


def part1(data):
    """Solve part 1"""
    return data[0] # the largest sum


def part2(data):
    """Solve part 2"""
    return sum(data[:3]) # the sum of the top three


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
