import aoc

# data = aoc.getLinesForDay(5, force_filepath="inputs/day05_example.txt")
data = aoc.getLinesForDay(5)


instructions = []
for line in data:
    coord1, coord2 = line.split(" -> ")
    x1, y1 = [int(x) for x in coord1.split(",")]
    x2, y2 = [int(x) for x in coord2.split(",")]
    instructions.append((x1, y1, x2, y2))


def doTheCount(instructions, isPart1):
    # Make a dict of coordinates to occurence
    occurences = dict()

    for instr in instructions:
        x1, y1, x2, y2 = instr
        # print("=", x1, y1, x2, y2)
        if isPart1 and x1 != x2 and y1 != y2:
            print(x1, y1, x2, y2, "SKIP")
            continue

        dirX = 1 if x2 > x1 else -1
        dirY = 1 if y2 > y1 else -1

        deltaY = abs(y2 - y1)
        deltaX = abs(x2 - x1)

        rangeY = [y1] * (deltaX + 1) if deltaY == 0 else range(y1, y2 + dirY, dirY)
        rangeX = [x1] * (deltaY + 1) if deltaX == 0 else range(x1, x2 + dirX, dirX)

        # print("RANGES", rangeX, rangeY)

        for _x, _y in zip(rangeX, rangeY):
            coord = (_x, _y)
            if coord not in occurences:
                occurences[coord] = 0
            occurences[coord] += 1

    """ Debug display

    minX = min([x for x, y in occurences.keys()])
    maxX = max([x for x, y in occurences.keys()])
    minY = min([y for x, y in occurences.keys()])
    maxY = max([y for x, y in occurences.keys()])

    gridStr = ""
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            gridStr += str(occurences[(x, y)]) if (x, y) in occurences else "."
        gridStr += "\n"
    print(gridStr)

    # """

    count_2_or_more = 0
    for val in occurences.items():
        if val >= 2:
            count_2_or_more += 1

    return count_2_or_more


# Part 1

print("Part 1", doTheCount(instructions, True))

# 7284 too low

# Part 2

print("Part 2", doTheCount(instructions, False))

# first try (by noticing that the example answer was wrong)