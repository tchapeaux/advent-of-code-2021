import heapq
import time

import aoc

start_time = time.time()

cells = aoc.getNumberCellsForDay(15)


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

# This still took 3 minutes to get the answer, so looking into it a bit more and:
# I removed the heuristic (not useful because in Part 2 we search the whole board anyway)
# I used the heapq more efficiently (without re-prioritizing at each step)
# This wastes memory ( :shrug: ), but the solution is found 100x faster, so it seems worth it


def getShortestPathValue(cells):

    print("Searching path for grid of size")
    print(len(cells), "x", len(cells[0]))

    # define constants and data structure

    # Start and Stop cells
    START = (0, 0)
    STOP = (len(cells) - 1, len(cells) - 1)

    # Set containing all "visited" cells
    visited = set()

    # Dictionary of cell containing current shortest distance known
    shortest_known_distance = {START: 0}
    # heapq of the "frontier", ie. the next cells to visit ordered by priority
    priorityQueue = [[0, START]]

    # Main loop: explore each cell of the frontier and add new neighbors
    while STOP not in visited:
        if len(visited) % 10000 == 0:
            print(len(visited), time.time() - start_time)

        # get nearest unvisited node
        _, nearest = heapq.heappop(priorityQueue)
        nearestPathValue = shortest_known_distance[nearest]

        # Check its neighbors
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
                # Here we simply add a new entry to the heapq
                # this means duplicate entries are possible, but this is not an
                # issue as checking an entry a second time will have no effect
                heapq.heappush(
                    priorityQueue,
                    [neighPathValue, neighCoord],
                )

        # Mark cell as visited
        visited.add(nearest)
        shortest_known_distance[nearest] = nearestPathValue

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