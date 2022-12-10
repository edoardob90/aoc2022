# pylint: disable=invalid-name
"""AoC day 5, 2022"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    stacks, moves = puzzle_input.split("\n\n")

    stacks = stacks.splitlines()
    stacks, cols = stacks[:-1], len(stacks[-1].split())

    # read the moves list
    moves = list(
        map(
            lambda move: re.match(r"move (\d+) from (\d) to (\d)", move).groups(),
            moves.splitlines(),
        )
    )

    def cleanup(line):
        return re.sub(r"[\[\]\s]+", "", re.sub(r"(\s?)\s{3}(\s?)", r"\1[.]\2", line))

    # read the crates stacks
    matrix = [cleanup(line) for line in stacks]

    # add extra rows to obtain a square matrix
    if (rows := len(matrix)) < cols:
        matrix = ["." * cols] * (cols - rows) + matrix

    # reverse
    matrix = [list(line) for line in matrix[::-1]]

    # transpose
    matrix = [list(filter(lambda x: x != ".", i)) for i in zip(*matrix)]

    return matrix, moves


def part1(data):
    """Solve part 1"""
    stacks, moves = data
    for num, src, dest in moves:
        s, d, n = int(src) - 1, int(dest) - 1, int(num)
        for _ in range(n):
            stacks[d].append(stacks[s].pop())
    return "".join(map(lambda x: x[-1], stacks))


def part2(data):
    """Solve part 2"""
    stacks, moves = data
    for num, src, dest in moves:
        s, d, n = int(src) - 1, int(dest) - 1, int(num)
        stacks[d].extend(stacks[s][-n:])
        del stacks[s][-n:]
    return "".join(map(lambda x: x[-1], stacks))


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    solution1 = part1(parse(puzzle_input))
    # need to re-read the input because Part 1 modified data in-place!
    solution2 = part2(parse(puzzle_input))

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text())
        print("\n".join(str(solution) for solution in solutions))
