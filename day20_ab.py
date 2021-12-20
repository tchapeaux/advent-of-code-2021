import aoc

data = aoc.getInputForDay(20)

algorithm, inputData = data.split("\n\n")

assert len(algorithm) == 512
# assert algorithm[0] == "."  # otherwise a square of empties will be lit

litPixels = set()

for rowIdx, row in enumerate(inputData.strip().split("\n")):
    for colIdx, cell in enumerate(row.strip()):
        if cell == "#":
            litPixels.add((colIdx, rowIdx))
        else:
            assert cell == "."


def get9Around(coord):
    yield (coord[0] - 1, coord[1] - 1)
    yield (coord[0], coord[1] - 1)
    yield (coord[0] + 1, coord[1] - 1)
    yield (coord[0] - 1, coord[1])
    yield (coord[0], coord[1])
    yield (coord[0] + 1, coord[1])
    yield (coord[0] - 1, coord[1] + 1)
    yield (coord[0], coord[1] + 1)
    yield (coord[0] + 1, coord[1] + 1)


def doEnhance(litPixels, outOfBoundsValue="."):
    newLitPixels = set()

    minX = min([c[0] for c in litPixels])
    maxX = max([c[0] for c in litPixels])
    minY = min([c[1] for c in litPixels])
    maxY = max([c[1] for c in litPixels])

    for y in range(minY - 1, maxY + 2):
        for x in range(minX - 1, maxX + 2):
            testedPixel = (x, y)
            pxlStr = ""
            for aroundCoord in get9Around(testedPixel):
                if (
                    aroundCoord[0] < minX
                    or aroundCoord[0] > maxX
                    or aroundCoord[1] < minY
                    or aroundCoord[1] > maxY
                ):
                    pxlStr += "1" if outOfBoundsValue == "#" else "0"
                else:
                    pxlStr += "1" if aroundCoord in litPixels else "0"

            value = int(pxlStr, 2)
            output = algorithm[value]
            if output == "#":
                newLitPixels.add(testedPixel)
            else:
                assert output == "."

    return newLitPixels


print(len(litPixels), "lit pixels")

savePart1 = None
currentIteration = litPixels
for step in range(50):
    print("Iteration", step + 1)
    currentIteration = doEnhance(
        currentIteration, outOfBoundsValue="." if step % 2 == 0 else "#"
    )
    print(len(currentIteration), "lit pixels")
    if step == 1:
        savePart1 = len(currentIteration)


# Part 1 : 5705 too high

print("Part 1", savePart1)
print("Part 2", len(currentIteration))
