# pylint: disable=invalid-name
"""AoC day 7, 2022"""

# Standard library imports
import pathlib
import sys
from collections import defaultdict


def parse(puzzle_input):
    """Parse input"""
    paths = []
    sizes = defaultdict(int)
    for line in puzzle_input.splitlines():
        words = line.strip().split()
        if words[1] == "cd":
            if words[2] == "..":
                paths.pop()
            else:
                paths.append(words[2])
        elif words[1] == "ls" or words[0] == "dir":
            continue
        else:
            size = int(words[0])
            for i in range(1, len(paths) + 1):
                sizes["/".join(paths[:i])] += size
    return sizes


def part1(data):
    """Solve part 1"""
    total = 0
    for size in data.values():
        if size <= 100_000:
            total += size
    return total


def part2(data):
    """Solve part 2"""
    avail = 70_000_000
    needed = 30_000_000
    max_used = avail - needed
    free = data["/"] - max_used
    candidates = list(filter(lambda s: s >= free, data.values()))
    return sorted(candidates)[0]


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
