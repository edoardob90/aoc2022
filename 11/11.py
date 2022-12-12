# pylint: disable=invalid-name
"""AoC day 11, 2022: Monkey in the Middle"""

# Standard library imports
import pathlib
import sys
import re
from functools import partial
from math import prod


def op(arg, operand=None, op_type=None):
    """Define operation"""
    if not operand:
        return arg**2
    if op_type == "*":
        return arg * int(operand)
    if op_type == "+":
        return arg + int(operand)
    return None


def parse(puzzle_input):
    """Parse input"""
    monkey_re = re.compile(
        r"Monkey (?P<idx>\d+):\n"
        r"\s+Starting items: (?P<items>.*?)\n"
        r"\s+Operation: new = (?P<op>.*?)\n\s"
        r"+Test: divisible by (?P<test>\d+)\n"
        r"\s.*true.*?(?P<true>\d+).*?(?P<false>\d+)",
        re.MULTILINE | re.DOTALL,
    )
    monkeys = {}
    puzzle_input = puzzle_input.split("\n\n")
    for monkey in puzzle_input:
        if match := monkey_re.match(monkey.strip()):
            props = match.groupdict()
            idx = props.pop("idx")
            # re-arrange items to be a list of int
            props["items"] = list(map(int, props["items"].split(", ")))
            # exctract the operation
            _op = props.pop("op").split()
            if _op[0] == _op[-1]:
                op_type = operand = None
            else:
                operand = _op[2]
                op_type = _op[1]
            # create a new monkey
            monkeys[idx] = props
            monkeys[idx]["op"] = partial(op, operand=operand, op_type=op_type)
            monkeys[idx]["count"] = 0

    return monkeys


def monkey_turn(monkeys, part, divisors):
    """Run a monkey game round"""
    for monkey in monkeys.values():
        while monkey["items"]:
            monkey["count"] += 1
            # perform the operation
            item = monkey["op"](monkey["items"].pop(0))
            if part == 1:
                # Part 1
                item //= 3
            elif part == 2:
                # Part 2
                item %= divisors
            # test and send item
            test, true, false = monkey["test"], monkey["true"], monkey["false"]
            if item % int(test) == 0:
                monkeys[true]["items"].append(item)
            else:
                monkeys[false]["items"].append(item)

    return monkeys


def run_game(monkeys, rounds=20, part=1):
    """Run a game"""
    divisors = prod([int(m["test"]) for m in monkeys.values()])
    counts = []
    for _ in range(rounds):
        monkeys = monkey_turn(monkeys, part, divisors)

    for monkey in monkeys.values():
        counts.append(monkey["count"])

    a, b = sorted(counts, reverse=True)[:2]

    return a * b


def part1(data):
    """Solve part 1"""
    return run_game(data, 20, part=1)


def part2(data):
    """Solve part 2"""
    return run_game(data, 10_000, part=2)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    solution1 = part1(parse(puzzle_input))
    solution2 = part2(parse(puzzle_input))

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
