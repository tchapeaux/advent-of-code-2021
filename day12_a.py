import aoc

data = aoc.getLinesForDay(12)
# data = aoc.getLinesForDay(12, force_filepath="inputs/day12_mini_example.txt")


class Node(object):
    def __init__(self, name, neighs=None):
        self.name = name
        self.neighs = neighs if neighs else set()

    def __repr__(self):
        return f"N({self.name})"


nodeDict = {}

START = "start"
END = "end"


def isBigCave(node):
    return "A" <= node.name[0] <= "Z"


for line in data:
    pathFrom, pathTo = line.split("-")
    if pathFrom not in nodeDict:
        nodeDict[pathFrom] = Node(pathFrom)
    if pathTo not in nodeDict:
        nodeDict[pathTo] = Node(pathTo)
    fromNode = nodeDict[pathFrom]
    toNode = nodeDict[pathTo]
    fromNode.neighs.add(toNode)
    toNode.neighs.add(fromNode)

assert START in nodeDict and len(nodeDict[START].neighs) > 0
assert END in nodeDict and len(nodeDict[END].neighs) > 0

bigCaves = [c for c in nodeDict.values() if isBigCave(c)]
smallCaves = [c for c in nodeDict.values() if not isBigCave(c)]

print(
    "Found, big, small",
    len(nodeDict),
    len(bigCaves),
    len(smallCaves),
)


# Iterate through all paths


def isFullPath(path):
    return (
        path[0] == nodeDict[START]
        and path[-1] == nodeDict[END]
        and not isInvalidPath(path)
    )


def isInvalidPath(path):
    return any([path.count(c) > 1 for c in smallCaves])


def findFullPaths(currentPath):
    # print("current path", ",".join([n.name for n in currentPath]))

    currentNode = currentPath[-1]
    # print("\tcurrent node", currentNode.name)
    for neigh in currentNode.neighs:
        # print("\t\tneigh", neigh.name)
        newPath = [n for n in currentPath] + [neigh]
        if isInvalidPath(newPath):
            continue
        if neigh is nodeDict[END] and isFullPath(newPath):
            yield newPath
        else:
            for subsequentPath in findFullPaths(newPath):
                yield subsequentPath


foundPaths = list(findFullPaths([nodeDict[START]]))


for path in foundPaths:
    print(",".join([n.name for n in path]))

print("Part 1", len(foundPaths), "paths")
