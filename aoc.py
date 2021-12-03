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

import requests
from dotenv import load_dotenv

load_dotenv()


YEAR = os.environ["YEAR"]
AOC_TOKEN = os.environ["AOC_TOKEN"]


def urlForDay(dayNbr):
    return f"https://adventofcode.com/{YEAR}/day/{dayNbr}/input"


def filepathForDay(dayNbr):
    return f"inputs/day{dayNbr}_input.txt"


def getInputForDay(dayNbr, force_filepath=None):
    if force_filepath:
        with open(force_filepath) as f:
            return f.read()

    filepath = filepathForDay(dayNbr)
    if not os.path.exists(filepath):
        url = urlForDay(dayNbr)
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
