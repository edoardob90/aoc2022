# pylint: disable=invalid-name
"""AoC day 6, 2022"""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """Parse input"""
    return list(puzzle_input)


def partition(l, n, d=None, upto=True):
    """Generate sublists of `l` with length up to `n` and offset `d`"""
    offset = d or n
    return [
        lx for i in range(0, len(l), offset) if upto or len(lx := l[i : i + n]) == n
    ]


def part1(data):
    """Solve part 1"""
    pdata = list(map(set, partition(data, n=4, d=1, upto=False)))
    marker = list(filter(lambda x: len(x) == 4, pdata))[0]
    return ("".join(data)).find("".join(marker)) + 4


def part2(data):
    """Solve part 2"""
    pdata = list(map(set, partition(data, n=14, d=1, upto=False)))
    marker = list(filter(lambda x: len(x) == 14, pdata))[0]
    return ("".join(data)).find("".join(marker)) + 14


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
