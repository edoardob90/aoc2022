# pylint: disable=invalid-name
"""AoC day 13, 2022: Distress Signal"""

# Standard library imports
import pathlib
import sys
from functools import cmp_to_key


def parse(puzzle_input):
    """Parse input"""
    puzzle_input = puzzle_input.split("\n\n")
    puzzle_input = [p.split("\n") for p in puzzle_input]
    return [list(map(eval, p)) for p in puzzle_input]


def compare(p1, p2):
    """Compare two packets"""
    # (1) check if both args are integers
    if isinstance(p1, int):
        if isinstance(p2, int):
            # < 0 means correct ordering
            # 0 means undefined
            # > 0 wrong ordering
            return p1 - p2
        # (2a) 'p2' must be a list, but 'p1' is not
        p1 = [p1]

    # (2b) 'p1' must be a list; 'p2' must be as well if it's not already
    if isinstance(p2, int):
        p2 = [p2]

    # (3) recursively compare two lists
    for x, y in zip(p1, p2):
        if (r := compare(x, y)):
            return r

    # (4) compare lengths
    return len(p1) - len(p2)


def part1(data):
    """Solve part 1"""
    right_order = []
    for i, pair in enumerate(data, start=1):
        if compare(*pair) < 0:
            right_order.append(i)
    return sum(right_order)


def part2(data):
    """Solve part 2"""
    unroll = []
    # add the extra packets
    unroll.extend([[[2]], [[6]]])

    for x, y in data:
        unroll.extend([x, y])

    unroll.sort(key=cmp_to_key(compare))

    return (1 + unroll.index([[2]])) * (1 + unroll.index([[6]]))


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
