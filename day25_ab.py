import copy
import aoc

data = aoc.getCellsForDay(25)
# data = aoc.getCellsForDay(25, force_filepath="inputs/day25_example.txt")
# data = aoc.getCellsForDay(25, force_filepath="inputs/day25_mini_example.txt")

HEIGHT = len(data)
WIDTH = len(data[0])
assert all(len(row) == WIDTH for row in data)


def printGrid(grid):
    for row in grid:
        print("".join(row))


def getNextPosition(grid, currentPos):
    sc = grid[currentPos[1]][currentPos[0]]
    if sc == "v":
        y = (currentPos[1] + 1) % len(grid)
        x = currentPos[0]
    else:
        assert sc == ">"
        y = currentPos[1]
        x = (currentPos[0] + 1) % len(grid[y])
    return grid[y][x], (x, y)


grid = data

step = 0
hasMoved = True
while hasMoved:
    newGrid = copy.deepcopy(grid)
    step += 1
    print("Step", step)
    # printGrid(grid)

    hasMoved = False

    # Check EAST-facing first
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if grid[y][x] == ">":
                adjValue, nextPosition = getNextPosition(grid, (x, y))
                if adjValue == ".":
                    # print("Moving", (x, y), "to", nextPosition)
                    hasMoved = True
                    newGrid[nextPosition[1]][nextPosition[0]] = ">"
                    newGrid[y][x] = "."

    grid = newGrid
    newGrid = copy.deepcopy(grid)

    # Check SOUTH-facing second
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if grid[y][x] == "v":
                adjValue, nextPosition = getNextPosition(grid, (x, y))
                if adjValue == ".":
                    # print("Moving", (x, y), "to", nextPosition)
                    hasMoved = True
                    newGrid[nextPosition[1]][nextPosition[0]] = "v"
                    newGrid[y][x] = "."

    grid = newGrid

print("Part 1", step)
