import heapq
import time

import aoc

start_time = time.time()

cells = aoc.getNumberCellsForDay(15)

print("size", len(cells), len(cells[0]))


def manhattanDistance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(y2 - y1) + abs(x2 - x1)


# What we want to do (Initial notes before starting):
# exploring all paths by maintaning a list of "edge" nodes and iterating over the path from shortest to longest
# When we reach the end Tile, we are sure it's the shortest path
# This works because there are no negative path
# (I think this is Dijkstra? My memory is fading)

# Finally I looked up the Dijkstra pseudo-code on Wikipedia :+1:

# Dijkstra was OK for Part 1 but Part 2 needed something else
# The solution below uses two optimisations on basic Dijkstra:
# 1 - Use heuristic to help Dijkstra pick the best "next candidate"
# 2 - Use a Python heapq to manage the priorities


def getShortestPathValue(cells):

    START = (0, 0)
    STOP = (len(cells) - 1, len(cells) - 1)

    visited = set()

    # heapq where the items are tuple
    # item[0] is the distance and item[1] is the node
    shortest_known_distance = {START: 0}
    priorityQueue = [[manhattanDistance(START, STOP), START]]

    while STOP not in visited:
        if len(visited) % 10000 == 0:
            print(len(visited), time.time() - start_time)

        # get nearest unvisited node
        _, nearest = heapq.heappop(priorityQueue)
        nearestPathValue = shortest_known_distance[nearest]

        # Check neighbors
        neighbors = list(aoc.get4Neighbors(cells, nearest[0], nearest[1]))
        for neighX, neighY, value in neighbors:
            neighCoord = (neighX, neighY)
            if neighCoord in visited:
                continue

            neighPathValue = nearestPathValue + value

            # Update shortest known distance
            if (
                neighCoord not in shortest_known_distance
                or shortest_known_distance[neighCoord] > neighPathValue
            ):
                shortest_known_distance[neighCoord] = neighPathValue

            # Update priority
            neighEntry = [x for x in priorityQueue if x[1] == neighCoord]
            neighPriority = neighPathValue + manhattanDistance(neighCoord, STOP)
            if len(neighEntry) == 0:
                heapq.heappush(
                    priorityQueue,
                    [neighPriority, neighCoord],
                )
            elif neighEntry[0][0] > neighPriority:
                neighEntry[0][0] = neighPriority
                # refresh the heap because we changed a priority manually
                heapq.heapify(priorityQueue)

        # Marked as visited
        visited.add(nearest)
        shortest_known_distance[nearest] = nearestPathValue - manhattanDistance(
            nearest, STOP
        )

    print("Visited", len(visited), "nodes")
    return shortest_known_distance[STOP]


print("Part 1", getShortestPathValue(cells))

# Create grid for part 2


SIZE = len(cells)
biggerCells = []
for y in range(SIZE * 5):
    tileY = y // SIZE
    biggerCells.append([])
    for x in range(SIZE * 5):
        tileX = x // SIZE
        value = cells[x % SIZE][y % SIZE] + tileY + tileX
        while value > 9:
            value -= 9
        biggerCells[-1].append(value)

print("Part 2", getShortestPathValue(biggerCells))