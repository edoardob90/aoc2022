#!/usr/bin/env python
# pylint: disable=invalid-name,too-many-locals,unspecified-encoding
"""AoC day 25, 2022: Full of Hot Air"""

## Standard library imports
import pathlib
import sys

## Third-party
# from codetiming import Timer


def parse_data(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


# @Timer(name="Part 1", text="{name}: {milliseconds:.1f} ms")
def part1(data):
    """Solve part 1"""
    # convert to decimal and calculate the total
    total = 0
    for num in data:
        coeff = 1
        for n in num[::-1]:
            total += ("=-012".find(n) - 2) * coeff
            coeff *= 5

    # convert to SNAFU
    result = ""
    while total:
        r = total % 5
        total //= 5

        if r <= 2:
            result = str(r) + result
        else:
            # if the remainder is > 2, we subtract 5 and add it to the next digit
            # "next" means with a higher power of the base
            # example in base 10: we could write 21 as "1(11)", but 11 is > 10
            # so we subtract 10 and add it to the tenth = 2 * 10 + (11 - 10) = 21
            result = "   =-"[r] + result
            total += 1

    return result


# @Timer(name="Part 2", text="{name}: {milliseconds:.1f} ms")
def part2(data):
    """Solve part 2"""
    return "It's Christmas Day, there's no part 2! 🎉"


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse_data(puzzle_input)
    yield part1(data)
    yield part2(data)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
