import aoc
import copy

data = aoc.getLinesForDay(22)
# data = aoc.getLinesForDay(22, force_filepath="inputs/day22_example.txt")
# data = aoc.getLinesForDay(22, force_filepath="inputs/day22_customexample.txt")

rules = []
for line in data:
    targetMode, coordsStr = line.split(" ")
    coords = []
    for coord in coordsStr.split(","):
        coord = coord[2:]  # remove x=
        coordMin, coordMax = coord.split("..")

        coords.append((int(coordMin), int(coordMax)))
        assert coords[-1][0] <= coords[-1][1]

    rules.append((targetMode, coords[0], coords[1], coords[2]))


class Region(object):
    def __init__(self, minX, maxX, minY, maxY, minZ, maxZ):
        assert minX <= maxX
        self.minX = minX
        self.maxX = maxX
        assert minY <= maxY
        self.minY = minY
        self.maxY = maxY
        assert minZ <= maxZ
        self.minZ = minZ
        self.maxZ = maxZ

    def __repr__(self):
        return f"R({self.minX}, {self.maxX}, {self.minY}, {self.maxY}, {self.minZ}, {self.maxZ})"

    def __len__(self):
        return (
            (self.maxX - self.minX + 1)
            * (self.maxY - self.minY + 1)
            * (self.maxZ - self.minZ + 1)
        )

    def intersects(self, other):
        return not (
            other.minX > self.maxX
            or other.maxX < self.minX
            or other.minY > self.maxY
            or other.maxY < self.minY
            or other.minZ > self.maxZ
            or other.maxZ < self.minZ
        )

    def isFullyContainedIn(self, other):
        return (
            other.minX <= self.minX
            and other.maxX >= self.maxX
            and other.minY <= self.minY
            and other.maxY >= self.maxY
            and other.minZ <= self.minZ
            and other.maxZ >= self.maxZ
        )

    def decomposeAround(self, other):
        """ returns 6 sub-regions of self around other """
        # The 6 regions correspond to the 6 faces of self
        # UP DOWN LEFT RIGHT BACK FRONT
        # what about "diagonal regions", you ask??
        # UP and DOWN (y) will actually contain "everything above and below" (expanding in x and z)
        # LEFT and RIGHT (x) will contain slices expanding in the z direction as well
        # and BACK and FRONT (z) will only contain the remaining slices

        assert self.intersects(other)

        upRegion = None
        if other.minY > self.minY:
            upRegion = copy.deepcopy(self)
            upRegion.maxY = other.minY - 1

        downRegion = None
        if other.maxY < self.maxY:
            downRegion = copy.deepcopy(self)
            downRegion.minY = other.maxY + 1

        leftRegion = None
        if other.minX > self.minX:
            leftRegion = copy.deepcopy(self)
            if upRegion:
                leftRegion.minY = upRegion.maxY + 1
            if downRegion:
                leftRegion.maxY = downRegion.minY - 1
            leftRegion.maxX = other.minX - 1

        rightRegion = None
        if other.maxX < self.maxX:
            rightRegion = copy.deepcopy(self)
            if upRegion:
                rightRegion.minY = upRegion.maxY + 1
            if downRegion:
                rightRegion.maxY = downRegion.minY - 1
            rightRegion.minX = other.maxX + 1

        backRegion = None
        if other.minZ > self.minZ:
            backRegion = copy.deepcopy(self)
            if upRegion:
                backRegion.minY = upRegion.maxY + 1
            if downRegion:
                backRegion.maxY = downRegion.minY - 1
            if leftRegion:
                backRegion.minX = leftRegion.maxX + 1
            if rightRegion:
                backRegion.maxX = rightRegion.minX - 1
            backRegion.maxZ = other.minZ - 1

        frontRegion = None
        if other.maxZ < self.maxZ:
            frontRegion = copy.deepcopy(self)
            if upRegion:
                frontRegion.minY = upRegion.maxY + 1
            if downRegion:
                frontRegion.maxY = downRegion.minY - 1
            if leftRegion:
                frontRegion.minX = leftRegion.maxX + 1
            if rightRegion:
                frontRegion.maxX = rightRegion.minX - 1
            frontRegion.minZ = other.maxZ + 1

        return upRegion, downRegion, leftRegion, rightRegion, backRegion, frontRegion


def addRegionToRegionSet(regionSet, newRegion):
    """
    Add the region and clean the regionSet to remove intersections.
    Note:
    - assumes regionSet is already clean
    """
    nonIntersectingRegions = set()

    for region in regionSet:
        if region.isFullyContainedIn(newRegion):
            continue

        if newRegion.isFullyContainedIn(region):
            # adding the new region does not modify the set, so return it
            return regionSet

        if region.intersects(newRegion):
            # divide new region in chuncks and try again
            subregions = newRegion.decomposeAround(region)
            subregions = [r for r in subregions if r]
            newRegionSet = copy.deepcopy(regionSet)
            for subR in subregions:
                newRegionSet = addRegionToRegionSet(newRegionSet, subR)
            return newRegionSet
        else:
            nonIntersectingRegions.add(region)

    nonIntersectingRegions.add(newRegion)
    return nonIntersectingRegions


onRegions = set()
for ruleIdx, rule in enumerate(rules):
    print("== rule", ruleIdx, "of", len(rules))
    print("current size", len(onRegions))
    print(rule)

    ruleRegion = Region(
        rule[1][0], rule[1][1], rule[2][0], rule[2][1], rule[3][0], rule[3][1]
    )

    if rule[0] == "on":
        onRegions = addRegionToRegionSet(onRegions, ruleRegion)
    else:
        assert rule[0] == "off"
        # cut a hole in existing regions
        newOnRegions = set()
        for region in onRegions:
            if region.intersects(ruleRegion):
                for subregion in region.decomposeAround(ruleRegion):
                    if subregion:
                        newOnRegions.add(subregion)
            else:
                newOnRegions.add(region)
        onRegions = newOnRegions


if len(onRegions) < 100:
    print(onRegions)

onSize = sum([len(r) for r in onRegions])


print("Part 2", onSize)

# 2 failed attempts
# first one caused me to rewrite my whole algorithm
# second one was because there was a bug in my too-complex new algorithm
# in the end I got it!