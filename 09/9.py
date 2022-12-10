# pylint: disable=invalid-name
"""AoC day 9, 2022: Rope Bridge"""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """Parse input"""
    moves = [line.strip().split() for line in puzzle_input.splitlines()]
    return moves


def move(H, T):
    """Adjust position of Tail w.r.t. Head, if need be"""
    xh, yh = H
    xt, yt = T

    dx = abs(xh - xt)
    dy = abs(yh - yt)

    if dx <= 1 and dy <= 1:
        # do nothing
        pass
    elif dx >= 2 and dy >= 2:
        # move both
        T = (xh - 1 if xt < xh else xh + 1, yh - 1 if yt < yh else yh + 1)
    elif dx >= 2:
        # move only x
        T = (xh - 1 if xt < xh else xh + 1, yh)
    elif dy >= 2:
        # move only y
        T = (xh, yh - 1 if yt < yh else yh + 1)

    return T


delta_x = {"L": 1, "R": -1, "U": 0, "D": 0}
delta_y = {"L": 0, "R": 0, "U": 1, "D": -1}


def part1(data):
    """Solve part 1"""
    H = (0, 0)
    T = (0, 0)
    tail_path = set([T])
    for direction, step in data:
        for _ in range(int(step)):
            # Update the head's position
            H = H[0] + delta_x[direction], H[1] + delta_y[direction]
            # Update the tail's position
            T = move(H, T)
            tail_path.add(T)

    return len(tail_path)


def part2(data):
    """Solve part 2"""
    H = (0, 0)
    T = [(0, 0) for _ in range(9)]
    tail_path = set([T[-1]])
    for direction, step in data:
        for _ in range(int(step)):
            # Update the head's position
            H = H[0] + delta_x[direction], H[1] + delta_y[direction]
            # Update the first point that follows the head
            T[0] = move(H, T[0])
            # Update the remaining points
            for i in range(1, 9):
                T[i] = move(T[i - 1], T[i])
            # Add the tail's position to the path
            tail_path.add(T[-1])

    return len(tail_path)


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
