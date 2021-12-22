import aoc
import math

data = aoc.getLinesForDay(22)

rules = []
for line in data:
    targetMode, coordsStr = line.split(" ")
    coords = []
    for coord in coordsStr.split(","):
        coord = coord[2:]  # remove x=
        coordMin, coordMax = coord.split("..")

        coords.append((int(coordMin), int(coordMax)))
        assert coords[-1][0] < coords[-1][1]

    rules.append((targetMode, coords[0], coords[1], coords[2]))


def getRuleSize(rule):
    sizeX = rule[1][1] - rule[1][0]
    sizeY = rule[2][1] - rule[2][0]
    sizeZ = rule[3][1] - rule[3][0]
    return sizeX * sizeY * sizeZ


def getBoundedCubes(rule):
    minX = max(rule[1][0], -50)
    maxX = min(rule[1][1], 50)
    minY = max(rule[2][0], -50)
    maxY = min(rule[2][1], 50)
    minZ = max(rule[3][0], -50)
    maxZ = min(rule[3][1], 50)

    for x in range(minX, maxX + 1):
        for y in range(minY, maxY + 1):
            for z in range(minZ, maxZ + 1):
                yield (x, y, z)


onCubes = set()
for ruleIdx, rule in enumerate(rules):
    assert rule[0] in ["on", "off"]
    print("rule", ruleIdx, "of", len(rules))
    print(rule[0], getRuleSize(rule))

    for x, y, z in getBoundedCubes(rule):
        if rule[0] == "on":
            onCubes.add((x, y, z))
        else:
            onCubes.discard((x, y, z))

print("Part 1", len(onCubes))