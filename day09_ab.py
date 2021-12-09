import aoc

data = aoc.getCellsForDay(9)

# convert everything to int
data = [[int(c) for c in row] for row in data]

# print(data)


def getNeighbors(grid, x, y):
    """ yield x, y, value or all neighbors"""
    if y > 0:
        yield (x, y - 1, grid[y - 1][x])
    if y < len(grid) - 1:
        yield (x, y + 1, grid[y + 1][x])
    if x > 0:
        yield (x - 1, y, grid[y][x - 1])
    if x < len(grid[y]) - 1:
        yield (x + 1, y, grid[y][x + 1])


riskValuesAcc = 0
lowPoints = []  # set of coordinates tuples

for y in range(len(data)):
    for x in range(len(data[0])):
        height = data[y][x]
        neighbors = getNeighbors(data, x, y)
        isLowPoint = all([height < neighVal for _, _, neighVal in neighbors])
        if isLowPoint:
            riskValuesAcc += height + 1
            lowPoints.append((x, y))

print("number of low points", len(lowPoints))

print("Part 1", riskValuesAcc)


# Part 2

# Each bassin corresponds to at least one low point
# (in the example we have 1 bassin = 1 low point, but I think there could be more?)
# so we will mark neighbors recursively until we cover each bassin

bassins = [set([p]) for p in lowPoints]

# check which bassins are still expanding so we have a finish condition
isStillExpanding = [True for _ in lowPoints]
while any(isStillExpanding):
    for basIdx, bas in enumerate(bassins):
        if not isStillExpanding[basIdx]:
            continue
        isStillExpanding[basIdx] = False  # reset it until we find a new point

        # check each member of the bassin and mark neighbors unless they are 9
        marked = set()
        for p in bas:
            for neighX, neighY, neighVal in getNeighbors(data, p[0], p[1]):
                if (neighX, neighY) not in bas and neighVal < 9:
                    marked.add((neighX, neighY))
                    isStillExpanding[basIdx] = True

                # if neighbor is another low point (!), merge the bassins
                # not sure if this will happen with input but just in case
                if (neighX, neighY) in lowPoints:
                    foundLowPointIdx = lowPoints.index((neighX, neighY))
                    if foundLowPointIdx != basIdx:
                        # If this is printed it means I was right
                        print("TCHAP WAS RIGHT there are merged bassins")
                        # ⌛ spoiler I was not right

                        # merge into ourselves (finder keeper)
                        bas.update(bassins[foundLowPointIdx])
                        # clear previous bassin
                        bassins[foundLowPointIdx] = set()
                        isStillExpanding[foundLowPointIdx] = False
        bas.update(marked)

# The above loop is pretty slow, it could be optimized
# However the solution is found in under 10s, so leaving it as-is

bassinsLength = sorted([len(b) for b in bassins])


print(
    "Part 2",
    bassinsLength[-5:],
    bassinsLength[-1] * bassinsLength[-2] * bassinsLength[-3],
)
