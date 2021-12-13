import aoc

data = aoc.getLinesForDay(13)


dots = set()
folds = []
for line in data:
    if "," in line:
        dot = tuple(int(x) for x in line.split(","))
        dots.add(dot)
    if "fold" in line:
        axis = line[11]  # Just hardocde it
        assert axis in "xy", axis
        value = int(line.split("=")[1])
        folds.append((axis, value))

for foldIdx, fold in enumerate(folds):
    axis, value = fold
    coord = 0 if axis == "x" else 1
    newDots = set()
    for dot in dots:
        if dot[coord] > value:
            delta = dot[coord] - value
            newDot = [None, None]
            newDot[coord] = value - delta
            newDot[1 - coord] = dot[1 - coord]
            newDots.add(tuple(newDot))
        else:
            newDots.add(dot)
    dots = newDots

    if foldIdx == 0:
        print("Part 1", len(dots))


# Display table

minX = min(d[0] for d in dots)
maxX = max(d[0] for d in dots)
minY = min(d[1] for d in dots)
maxY = max(d[1] for d in dots)


tableStr = ""
for y in range(minY, maxY + 1):
    for x in range(minX, maxX + 1):
        tableStr += "#" if (x, y) in dots else " "
    tableStr += "\n"

print(f"Part2\n{tableStr}")
