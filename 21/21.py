#!/usr/bin/env python
# pylint: disable=invalid-name,too-many-locals,unspecified-encoding
"""AoC day 21, 2022: Monkey Math"""

## Standard library imports
import pathlib
import sys
from operator import add, sub, truediv, mul

## Third-party
# from codetiming import Timer
import sympy


def parse_data(puzzle_input):
    """Parse input"""
    return puzzle_input.splitlines()


# @Timer(name="Part 1", text="{name}: {milliseconds:.1f} ms")
# ~67.6 ms
def part1(data):
    """Solve part 1"""
    monkeys = {}
    for line in data:
        name, arg = line.split(": ")
        if arg.isdigit():
            monkeys[name] = int(arg)
        else:
            left, op, right = arg.split()
            if left in monkeys and right in monkeys:
                monkeys[name] = eval(f"int({monkeys[left]} {op} {monkeys[right]})")
            else:
                # trick!
                # append the current line to data, to process it again some time later
                data.append(line)

    return monkeys["root"]


# @Timer(name="Part 2", text="{name}: {milliseconds:.1f} ms")
# ~496 ms
def part2(data):
    """Solve part 2"""
    monkeys = {"humn": sympy.Symbol("x")}

    ops = {"+": add, "-": sub, "*": mul, "/": truediv}

    for line in data:
        name, arg = line.split(": ")
        # if we already met this monkey, skip it
        # this also shields us from re-defining "humn", which will be a HUGE mistake
        if name in monkeys:
            continue

        if arg.isdigit():
            # use sympy.Integer to store infinite precision integer numbers
            monkeys[name] = sympy.Integer(arg)
        else:
            left, op, right = arg.split()
            if left in monkeys and right in monkeys:
                if name == "root":
                    # sympy.solve returns a list of solutions. here, there's only one
                    me = sympy.solve(monkeys[left] - monkeys[right])[0]
                    # print the equation instead of solving
                    # me = f"{monkeys[left]} - {monkeys[right]} = 0"
                    break
                monkeys[name] = ops[op](monkeys[left], monkeys[right])
            else:
                data.append(line)
    return me


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
