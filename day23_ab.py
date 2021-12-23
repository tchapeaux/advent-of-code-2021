import copy
import time

import aoc

data = aoc.getCellsForDay(23)


# Manually add the "empty" cells in the last two rows that are discarded by my automatic parser
data[3] = ["#", "#"] + data[3] + ["#", "#"]
data[4] = ["#", "#"] + data[4] + ["#", "#"]


AMPHIPOD_TYPES = "ABCD"

start_time = time.time()


def showState(grid):
    print("0123456789012")
    for row in grid:
        print("".join(row))


showState(data)

TARGET_COLUMNS = {"A": 3, "B": 5, "C": 7, "D": 9}
STEP_COST_BY_TYPE = {"A": 1, "B": 10, "C": 100, "D": 1000}


def isRoomFree(grid, amphiType):
    """ Return True if the room for amphiType is free """
    roomX = TARGET_COLUMNS[amphiType]
    for cell in [grid[y][roomX] for y in range(len(grid))]:
        if cell in AMPHIPOD_TYPES and cell is not amphiType:
            return False
    return True


class Amphipod(object):
    def __init__(self, type, position):
        assert type in AMPHIPOD_TYPES
        self.type = type
        assert len(position) == 2 and all([isinstance(x, int) for x in position])
        self.position = position
        self.targetColumn = TARGET_COLUMNS[type]

    def stepCost(self):
        return STEP_COST_BY_TYPE[self.type]

    def __repr__(self):
        return f"amp({self.type}, {self.position})"

    def isInFinalPosition(self, grid):
        if self.position[0] != self.targetColumn:
            return False

        x = self.position[0]
        for y in range(2, len(grid)):
            if y == self.position[1]:
                continue
            cellInColumn = grid[y][x]
            if cellInColumn in AMPHIPOD_TYPES and cellInColumn != self.type:
                return False

        return True

    def isInHallway(self):
        return self.position[1] == 1

    def canMove(self, grid):
        if self.isInFinalPosition(grid):
            return False

        if self.isInHallway():
            return isRoomFree(grid, self.type)

        # else:
        # Check if it's possible to go to the hallway
        for y in range(self.position[1] - 1, 0, -1):
            if grid[y][self.position[0]] != ".":
                return False

        return True

    def move(self, grid, newPosition, dryRun=False):
        """
        Update grid and returns the cost
        Otherwise returns -1 and do not modify grid
        """
        (x, y) = self.position
        (newX, newY) = newPosition
        directionX = 1 if newX > x else -1
        directionY = 1 if newY > y else -1
        assert not self.isInFinalPosition(grid)
        assert newPosition is not self.position

        pathCost = 0

        # Forbidden stopping place
        assert newPosition not in [(3, 1), (5, 1), (7, 1), (9, 1)]

        if newY == 1:
            # GOING UP
            assert directionY == -1
            assert y > 1
            # check path is not blocked
            for pathY in range(y - 1, newY - 1, -1):
                if grid[pathY][x] != ".":
                    return -1
                pathCost += self.stepCost()
            for pathX in range(x + directionX, newX + directionX, directionX):
                if grid[newY][pathX] != ".":
                    return -1
                pathCost += self.stepCost()
        elif y == 1:
            # GOING DOWN
            assert directionY == 1
            assert y == 1
            assert newX == self.targetColumn
            # check path is not blocked
            for pathX in range(x + directionX, newX + directionX, directionX):
                if grid[y][pathX] != ".":
                    return -1
                pathCost += self.stepCost()
            for pathY in range(y + 1, newY + 1):
                if grid[pathY][newX] != ".":
                    return -1
                pathCost += self.stepCost()

        else:
            # None of the start and target position are in the buffer zone
            # So this is a full UP + LEFT/RIGHT + DOWN
            for pathY in range(y - 1, 0, -1):
                if grid[pathY][x] != ".":
                    return -1
                pathCost += self.stepCost()
            for pathX in range(x + directionX, newX + directionX, directionX):
                if grid[1][pathX] != ".":
                    return -1
                pathCost += self.stepCost()
            for pathY in range(1 + 1, newY + 1):
                if grid[pathY][newX] != ".":
                    return -1
                pathCost += self.stepCost()

        if not dryRun:
            # Do the move
            grid[y][x] = "."
            grid[newY][newX] = self.type
            self.position = (newX, newY)
            return pathCost


def getAmpFromGrid(grid):
    amphipods = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in AMPHIPOD_TYPES:
                a = Amphipod(cell, (x, y))
                amphipods.add(a)

    return amphipods


# Explore all possibilities recurvisely

PART_1_MAX_BOUND = 20000
bestKnownCost = PART_1_MAX_BOUND

fullyExploredStates = set()


def exploreNextMoves(grid, pastCost):
    # print("explore", pastCost)
    # showState(grid)

    global bestKnownCost
    if pastCost > bestKnownCost:
        # showState(grid)
        # print("BUSTED", pastCost)
        return

    amphipods = getAmpFromGrid(grid)
    stateAsTuple = tuple([a.position for a in amphipods] + [pastCost])

    if stateAsTuple in fullyExploredStates:
        # print("I've seen this before", len(fullyExploredStates))
        return

    if all([amp.isInFinalPosition(grid) for amp in amphipods]):
        # STOP
        # record score
        if pastCost < bestKnownCost:
            print("FOUND PATH WITH COST", pastCost)
            bestKnownCost = pastCost
        return

    amphipods = [
        a for a in amphipods if not a.isInFinalPosition(grid) and a.canMove(grid)
    ]

    amphipods = sorted(amphipods, key=lambda a: a.type)

    # First try to move from the hallway to the room
    for amp in amphipods:
        if amp.isInHallway() and isRoomFree(grid, amp.type):
            # Try to move into the room

            gridCopy = copy.deepcopy(grid)
            ampCopy = copy.deepcopy(amp)

            x = TARGET_COLUMNS[amp.type]
            # Find target y position
            # = lowest free position
            y = len(gridCopy) - 1
            while gridCopy[y][x] != ".":
                y -= 1
            moveCost = ampCopy.move(gridCopy, (x, y))

            if moveCost > 0:
                # print("Move", amp, "into its room")
                exploreNextMoves(gridCopy, pastCost + moveCost)

    # Second try to get some out
    for amp in amphipods:
        if not amp.isInHallway():
            waitingLocations = [(x, 1) for x in [1, 2, 4, 6, 8, 10, 11]]
            for waitLoc in waitingLocations:
                if waitLoc is amp.position:
                    continue

                if grid[waitLoc[1]][waitLoc[0]] == ".":

                    gridCopy = copy.deepcopy(grid)
                    ampCopy = copy.deepcopy(amp)

                    moveCost = ampCopy.move(gridCopy, (waitLoc))

                    if moveCost > 0:
                        # print("Move", amp, "into the hallway at", waitLoc)
                        exploreNextMoves(gridCopy, pastCost + moveCost)

    # print("<- Back in time")
    fullyExploredStates.add(stateAsTuple)


exploreNextMoves(data, 0)
print("It only took", time.time() - start_time)
print("Part 1", bestKnownCost)

# 12521 too high (kinda submitted the example value as a joke because I didn't find any lower ones)

# Construct the new grid for Part 2
dataPart2 = [
    data[0],
    data[1],
    data[2],
    ["#", "#", "#", "D", "#", "C", "#", "B", "#", "A", "#", "#", "#"],
    ["#", "#", "#", "D", "#", "B", "#", "A", "#", "C", "#", "#", "#"],
    data[3],
    data[4],
]

# Reinitialize values
PART_2_MAX_BOUND = 50000
bestKnownCost = 50000
fullyExploredStates = set()

showState(dataPart2)

exploreNextMoves(dataPart2, 0)
print("It only took", time.time() - start_time)
print("Part 2", bestKnownCost)


# 44169 too low -- I didn't realize all inputs were different (🙂) so using the example as max bound was not clever