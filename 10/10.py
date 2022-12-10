# pylint: disable=invalid-name
"""AoC day 10, 2022: Cathode-Ray Tube"""

# Standard library imports
import pathlib
import sys


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def run(instruction, register, cycle):
    """Run a given istruction, return the cycles spent in the execution"""
    if instruction == "noop":
        cycle += 1
    if instruction.startswith("addx"):
        _, arg = instruction.strip().split()
        register += int(arg)
        cycle += 2
    return cycle, register


def part1(data):
    """Solve part 1"""
    reg = 1
    cycle = strength = 0
    check = 20
    for instruction in data:
        prev = reg
        cycle, reg = run(instruction, reg, cycle)
        if cycle >= check:
            strength += check * prev
            check += 40
    return strength


def part2(data):
    """Solve part 2"""
    return data


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
