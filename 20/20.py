#!/usr/bin/env python
# pylint: disable=invalid-name,too-many-locals,unspecified-encoding
"""AoC day 20, 2022: Grove Positioning System"""

## Standard library imports
import pathlib
import sys

## Third-party
# from codetiming import Timer


class Node:
    """A single node of a doubly-linked list"""

    def __init__(self, n=None) -> None:
        self.n = n
        self.next = None
        self.prev = None


def parse_data(puzzle_input, factor=1):
    """Parse input"""
    data = [Node(int(n) * factor) for n in puzzle_input.splitlines()]
    for i, elem in enumerate(data):
        elem.next = data[(i + 1) % len(data)]
        elem.prev = data[(i - 1) % len(data)]
    return data


# @Timer(name="Part 1", text="{name}: {milliseconds:.1f} ms")
def part1(data):
    """Solve part 1"""
    # we'll loop over when shifting by N - 1 steps, where N is total number of elements
    bound = len(data) - 1

    for elem in data:
        if elem.n == 0:
            zero = elem
            continue

        target = elem
        if elem.n > 0:
            for _ in range(elem.n % bound):
                target = target.next

            if elem == target:
                continue

            # move elem right of target
            elem.next.prev = elem.prev
            elem.prev.next = elem.next

            target.next.prev = elem
            elem.next = target.next
            target.next = elem
            elem.prev = target
        else:
            for _ in range(-elem.n % bound):
                target = target.prev

            if elem == target:
                continue

            # move elem left of target
            elem.next.prev = elem.prev
            elem.prev.next = elem.next

            target.prev.next = elem
            elem.prev = target.prev
            target.prev = elem
            elem.next = target

    total = 0

    for _ in range(3):
        for _ in range(1000):
            zero = zero.next
        total += zero.n

    return total


# @Timer(name="Part 2", text="{name}: {milliseconds:.1f} ms")
def part2(data):
    """Solve part 2"""
    # we'll loop over when shifting by N - 1 steps, where N is total number of elements
    bound = len(data) - 1

    for _ in range(10):
        for elem in data:
            if elem.n == 0:
                zero = elem
                continue

            target = elem
            if elem.n > 0:
                for _ in range(elem.n % bound):
                    target = target.next

                if elem == target:
                    continue

                # move elem right of target
                elem.next.prev = elem.prev
                elem.prev.next = elem.next

                target.next.prev = elem
                elem.next = target.next
                target.next = elem
                elem.prev = target
            else:
                for _ in range(-elem.n % bound):
                    target = target.prev

                if elem == target:
                    continue

                # move elem left of target
                elem.next.prev = elem.prev
                elem.prev.next = elem.next

                target.prev.next = elem
                elem.prev = target.prev
                target.prev = elem
                elem.next = target

    total = 0

    for _ in range(3):
        for _ in range(1000):
            zero = zero.next
        total += zero.n

    return total


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    yield part1(parse_data(puzzle_input))
    yield part2(parse_data(puzzle_input, factor=811_589_153))


if __name__ == "__main__":
    for path in sys.argv[1:]:
        # print(f"\n{path}:")
        solutions = solve(puzzle_input=pathlib.Path(path).read_text().strip())
        print("\n".join(str(solution) for solution in solutions))
