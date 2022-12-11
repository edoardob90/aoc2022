# pylint: disable=invalid-name
"""AoC day 11, 2022: Monkey in the Middle"""

# Standard library imports
import pathlib
import sys
import re


def parse(puzzle_input):
    """Parse input"""
    monkey_re = re.compile(
        r"Monkey (?P<idx>\d+):\n\s+Starting items: (?P<items>.*?)\n\s+Operation: new = (?P<op>.*?)\n\s+Test: divisible by (?P<test>\d+)\n\s.*true.*?(?P<true>\d+).*?(?P<false>\d+)",
        re.MULTILINE | re.DOTALL,
    )
    monkeys = {}
    puzzle_input = puzzle_input.split("\n\n")
    for monkey in puzzle_input:
        if match := monkey_re.match(monkey.strip()):
            props = match.groupdict()
            props["items"] = list(map(int, props["items"].split(", ")))
            idx = props.pop("idx")
            monkeys[idx] = props
            monkeys[idx]["count"] = 0

    return monkeys


def monkey_turn(monkeys, relief=None):
    """Run a monkey game round"""
    for i, monkey in monkeys.items():
        # operation
        func_str = f"""def op(old):
            return {monkey['op']}"""
        exec(func_str, globals())
        func = globals()["op"]

        while items := monkey["items"]:
            monkey["count"] += 1
            # perform the operation
            item = items.pop(0)
            if relief:
                item = func(item) // relief
            # test and send item
            true, false = monkey["true"], monkey["false"]
            if item % int(monkey["test"]) == 0:
                monkeys[true]["items"].append(item)
            else:
                monkeys[false]["items"].append(item)

    return monkeys


def run_game(monkeys, rounds=20):
    """Run a game"""
    for _ in range(rounds):
        monkeys = monkey_turn(monkeys)
    return monkeys


def part1(data):
    """Solve part 1"""
    data = run_game(data, 20)
    counts = []
    for monkey in data.values():
        counts.append(monkey["count"])
    a, b = sorted(counts, reverse=True)[:2]
    return a * b


def part2(data):
    """Solve part 2"""
    return None


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
