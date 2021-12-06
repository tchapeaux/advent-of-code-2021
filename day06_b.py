import math

import aoc

import functools

data = aoc.getInputForDay(6)
# example
# data = "3,4,3,1,2"


# Part 2

fishes = [int(x) for x in data.split(",")]

REFRESH_TIME = 7
NEWBORN_COOLDOWN = 2


@functools.lru_cache(maxsize=256 * 8)
def countFish(currentTimer, remainingTicks, tabIndex=0, verbose=False):
    if verbose:
        print("\t" * tabIndex, "countFish", currentTimer, remainingTicks)

    count = 1

    if currentTimer >= remainingTicks:
        if verbose:
            print("\t" * (tabIndex + 1), "no child")
        return count

    directChildCount = 1 + math.floor(
        (remainingTicks - currentTimer - 1) / REFRESH_TIME
    )
    if verbose:
        print("\t" * (tabIndex + 1), "directChildCount", directChildCount)

    for childIdx in range(directChildCount):
        spawnTick = remainingTicks - currentTimer - childIdx * REFRESH_TIME
        if verbose:
            print("\t" * (tabIndex + 1), "child", childIdx, "born at", spawnTick)
        count += countFish(
            REFRESH_TIME,
            spawnTick - NEWBORN_COOLDOWN,
            tabIndex=tabIndex + 1,
            verbose=verbose,
        )

    return count


for dayCnt in range(257):
    count = sum([countFish(f, dayCnt, verbose=False) for f in fishes])
    print(dayCnt, count)
