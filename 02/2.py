# pylint: disable=invalid-name
"""AoC day 2, 2022"""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """
    Parse input

    Mapping:
      A = X = Rock (1 pt)
      B = Y = Paper (2 pt)
      C = Z = Scissors (3 pt)

    Rules:
      A beats C
      C beats B
      B beats A

    Points:
      lost = 0
      draw = 3
      win = 6
    """
    return puzzle_input.split("\n")


def part1(data):
    """Solve part 1"""
    POINTS = {"X": 1, "Y": 2, "Z": 3}

    total_points = 0

    for line in data:
        opp, me = line.split()
        total_points += POINTS[me]
        if opp == "A":
            if me == "X":
                total_points += 3
            elif me == "Y":
                total_points += 6
        elif opp == "B":
            if me == "Y":
                total_points += 3
            elif me == "Z":
                total_points += 6
        else:
            if me == "Z":
                total_points += 3
            elif me == "X":
                total_points += 6

    return total_points


def part2(data):
    """
    Solve part 2

    X = lose
    Y = draw
    Z = win
    """
    ENDS = {"X": 0, "Y": 3, "Z": 6}

    total_points = 0

    for line in data:
        opp, end = line.split()
        total_points += ENDS[end]
        if end == "X": # lose
            if opp == "A": # rock
                total_points += 3
            elif opp == "B": # paper
                total_points += 1
            else:
                total_points += 2
        elif end == "Y": # draw
            if opp == "A": # rock
                total_points += 1
            elif opp == "B": # paper
                total_points += 2
            else:
                total_points += 3
        else: # win
            if opp == "A": # rock
                total_points += 2
            elif opp == "B": # paper
                total_points += 3
            else:
                total_points += 1

    return total_points


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
