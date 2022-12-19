#!/usr/bin/env python
# pylint: disable=invalid-name,too-many-locals,unspecified-encoding,too-many-arguments
"""
AoC day 19, 2022: Not Enough Minerals

Need to hugely thank hyper-neutrino and jonathanpaulson for guiding me to the solution!
"""

## Standard library imports
import pathlib
import sys
import re
from math import ceil

## Third-party
from codetiming import Timer


def parse_data(puzzle_input):
    """
    Parse input

    Resource types are indexed with integers:
        0 = ore
        1 = clay
        2 = obsidian
        3 = geode
    """
    bps = []
    for line in puzzle_input.splitlines():
        bp = []
        maxspend = [0] * 3  # how much resources can we spend at each turn?

        for s in line.split(": ")[1].split("."):
            recipe = []

            if not (match := re.findall(r"(\d+) (\w+)", s)):
                continue

            for num, kind in match:
                num = int(num)
                kind = ("ore", "clay", "obsidian").index(kind)
                maxspend[kind] = max(maxspend[kind], num)
                recipe.append((num, kind))

            bp.append(recipe)

        bps.append((bp, maxspend))

    return bps


def how_many_geodes(bp, maxspend, cache, time, bots, res) -> int:
    """A DFS to compute the number of geodes we can produce in a given time"""
    # if there's no time left, return the actual number of geodes
    if time == 0:
        return res[3]

    key = tuple([time, *bots, *res])
    if key in cache:
        return cache[key]

    # there are 5 possible states:
    #   - build a bot collecting resources i   i=0,1,2,3
    #   - do nothing
    #
    # assume we're doing nothing: what's the max number of geodes?
    # it's the number of geodes we have + the number of geode-bot * remaining time
    maxval = res[3] + bots[3] * time

    # now calculate how many geodes we could have by producing each type of bot
    for bot_type, recipe in enumerate(bp):
        # OPTIMIZATION 1
        #   we skip if:
        #     (1) we're building a geode-bot
        #       and
        #     (2) we have more bots than the maximum we could spend of the resources they collect
        if bot_type != 3 and bots[bot_type] >= maxspend[bot_type]:
            continue

        # how much time we need to wait to have the resources to build a bot
        wait = 0

        for rcost, rtype in recipe:
            # if we don't have a bot of a given type, the waiting time would be infinite!
            if bots[rtype] == 0:
                break
            # the time needed is the cost MINUS resources we have DIVIDED BY how many bots can collect those resources
            time_needed = (rcost - res[rtype]) / bots[rtype]
            # compute the max waiting time
            wait = max(wait, ceil(time_needed))
        else:
            remaining = time - wait - 1

            # there's no point in building another bot if we have no time left
            if remaining <= 0:
                continue

            # amount of resources we have after 'wait' minutes
            res_ = [r + b * (wait + 1) for r, b in zip(res, bots)]

            # spend the resources to build a given bot
            for rcost, rtype in recipe:
                res_[rtype] -= rcost

            bots_ = bots[:]
            bots_[bot_type] += 1

            # OPTIMIZATION 2:
            #   we need to keep only the max resources we consume per round
            for i in range(3):
                res_[i] = min(res_[i], remaining * maxspend[i])

            maxval = max(
                maxval, how_many_geodes(bp, maxspend, cache, remaining, bots_, res_)
            )

    cache[key] = maxval

    return maxval


@Timer(name="Part 1", text="{name}: {seconds:.3f} s")
def part1(data):
    """Solve part 1"""
    total = 0

    for i, (bp, maxspend) in enumerate(data, start=1):
        max_geodes = how_many_geodes(bp, maxspend, {}, 24, [1, 0, 0, 0], [0] * 4)
        total += i * max_geodes

    return total


@Timer(name="Part 2", text="{name}: {seconds:.3f} s")
def part2(data):
    """Solve part 2"""
    total = 1

    for bp, maxspend in data[:3]:
        total *= how_many_geodes(bp, maxspend, {}, 32, [1, 0, 0, 0], [0] * 4)

    return total


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
