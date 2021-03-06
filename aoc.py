# Generic functions for use in the puzzles solutions
# Instructions:
# 1. Create a .env file and enter your session token as AOC_TOKEN=x (get it from the dev tools)
# 2. In your scripts, use the following functions:
#     - getInputForDay()    get the raw input
#     - getLinesForDay()    get the input line by line
#     - getCellsForday()    get a 2D table from the input
# If you want to test against the examples, create an example file and use the force_filepath option

# This solution stores the input files to avoid spamming the AoC server
# see https://www.reddit.com/r/adventofcode/comments/3v64sb/aoc_is_fragile_please_be_gentle/

import os


def urlForDay(year, dayNbr):
    return f"https://adventofcode.com/{year}/day/{dayNbr}/input"


def filepathForDay(dayNbr):
    dayStr = str(dayNbr).rjust(2, "0")
    return f"inputs/day{dayStr}_input.txt"


def getInputForDay(dayNbr, force_filepath=None):
    if force_filepath:
        with open(force_filepath) as f:
            return f.read()

    filepath = filepathForDay(dayNbr)
    if not os.path.exists(filepath):
        import requests
        from dotenv import load_dotenv

        load_dotenv()

        YEAR = os.environ["YEAR"]
        AOC_TOKEN = os.environ["AOC_TOKEN"]

        url = urlForDay(YEAR, dayNbr)
        cookies = dict(session=AOC_TOKEN)
        r = requests.get(url, cookies=cookies)
        with open(filepath, "w") as f:
            f.write(r.text)

    with open(filepath) as f:
        return f.read()


def getLinesForDay(dayNbr, force_filepath=None):
    raw = getInputForDay(dayNbr, force_filepath)
    return [l.strip() for l in raw.strip().split("\n")]


def getCellsForDay(dayNbr, force_filepath=None):
    linesInput = getLinesForDay(dayNbr, force_filepath)
    return [[c for c in l] for l in linesInput if len(l.strip()) > 0]


def getNumberCellsForDay(dayNbr, force_filepath=None):
    cellsInput = getCellsForDay(dayNbr, force_filepath)
    return [[int(c) for c in row] for row in cellsInput]


def get4Neighbors(grid, x, y):
    """ yield x, y, value for all N, S, E, W neighbors"""
    if y > 0:
        yield (x, y - 1, grid[y - 1][x])
    if y < len(grid) - 1:
        yield (x, y + 1, grid[y + 1][x])
    if x > 0:
        yield (x - 1, y, grid[y][x - 1])
    if x < len(grid[y]) - 1:
        yield (x + 1, y, grid[y][x + 1])


def get8Neighbors(grid, x, y):
    """ yield x, y, value for all N, S, E, W neighbors as well as NW, NE, SW, SE"""
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == dx == 0:
                continue
            if y + dy < 0 or y + dy > len(grid) - 1:
                continue
            if x + dx < 0 or x + dx > len(grid[y]) - 1:
                continue

            yield (x + dx, y + dy, grid[y + dy][x + dx])
