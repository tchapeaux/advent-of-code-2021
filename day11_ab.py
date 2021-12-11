import aoc

data = aoc.getCellsForDay(11)
# data = aoc.getCellsForDay(11, force_filepath="inputs/day11_example.txt")
# data = aoc.getCellsForDay(11, force_filepath="inputs/day11_mini_example.txt")

print("\n".join(["".join(row) for row in data]))
data = [[int(x) for x in row] for row in data]

NB_OF_STEPS = 500

flashAcc = 0
part1Solution = None

# For Part 2
NUMBER_OF_CELLS = len(data) * len(data[0])
part2Solution = None

for step in range(NB_OF_STEPS):
    print("Step", step + 1)

    # phase 1 - increase all cells by 1
    for y in range(len(data)):
        for x in range(len(data[y])):
            data[y][x] += 1

    # phase 2 - mark flashing cells
    # Because any flash can trigger new flashes,
    # this will be done in multiple iteration until all flashes are covered
    flashing = set()
    flashIsGrowingFlag = True
    while flashIsGrowingFlag:
        flashIsGrowingFlag = False
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] > 9 and (x, y) not in flashing:
                    flashIsGrowingFlag = True
                    flashing.add((x, y))
                    flashAcc += 1
                    for neighX, neighY, _ in aoc.get8Neighbors(data, x, y):
                        data[neighY][neighX] += 1

    print("flashed", len(flashing), "times")

    # phase 3 - power down flashing cells to 0
    for x, y in flashing:
        data[y][x] = 0

    # Check if one of the solution was reached
    if step == 99:
        part1Solution = flashAcc
    if len(flashing) == NUMBER_OF_CELLS and not part2Solution:
        part2Solution = step + 1


print("Part 1", part1Solution if part1Solution else flashAcc)

# 1760 too high

print("Part 2", part2Solution)

# 9992 too high