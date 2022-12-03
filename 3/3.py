# pylint: disable=invalid-name
"""AoC day 3, 2022"""

# Standard library imports
import pathlib
import sys
from string import ascii_lowercase, ascii_uppercase

prio = {l: i for i, l in enumerate(ascii_lowercase + ascii_uppercase, start=1)} # dict

def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split("\n")


def part1(data):
    """Solve part 1"""
    total = 0
    for line in data:
        mid = len(line) // 2
        first, second = set(line[:mid]), set(line[mid:])
        total += prio[(first & second).pop()] # with dict
    return total


def part2(data):
    """Solve part 2"""
    total = 0
    i = 0
    for line in data[::3]:
        group = set(line) & set(data[i+1]) & set(data[i+2])
        total += prio[group.pop()]
        i += 3
    return total


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
