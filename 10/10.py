# pylint: disable=invalid-name
"""AoC day 10, 2022: Cathode-Ray Tube"""

# Standard library imports
import pathlib
import sys

# From Day 6
def partition(l, n, d=None, upto=True):
    """Generate sublists of `l` with length up to `n` and offset `d`"""
    offset = d or n
    return [
        l[i : i + n] for i in range(0, len(l), offset) if upto or len(l[i : i + n]) == n
    ]


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


def run(instruction, register, cycle):
    """Run a given istruction, return the cycles spent in the execution"""
    if instruction == "noop":
        cycle += 1
    elif instruction.startswith("addx"):
        _, arg = instruction.strip().split()
        register += int(arg)
        cycle += 2
    return cycle, register


def part1(data):
    """Solve part 1"""
    reg = 1
    cycle = strength = pixel_pos = 0
    pixels = []
    check = 20
    for instruction in data:
        last_reg = reg
        cycle, reg = run(instruction, reg, cycle)

        if cycle >= check:
            strength += check * last_reg
            check += 40

        while pixel_pos < cycle:
            pixels.append(
                "#"
                if (pixel_pos % 40) >= last_reg - 1 and (pixel_pos % 40) <= last_reg + 1
                else "."
            )
            pixel_pos += 1

    return strength, pixels


def part2(data):
    """Solve part 2"""
    _, pixels = data
    screen = partition(pixels, 40)
    return "\n".join(map("".join, screen))


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(solution1)

    return solution1[0], solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
