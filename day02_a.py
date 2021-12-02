import aoc

data = aoc.getLinesForDay(2)

""""
data = [
    "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2",
]
# """

instructions = []
for line in data:
    [direction, value] = line.split(" ")
    instructions.append((direction, int(value)))

# print(instructions)

# Part 1

currentPosition = [0, 0]  # x, z

for (direction, value) in instructions:
    if direction == "up":
        currentPosition[1] -= value
    elif direction == "down":
        currentPosition[1] += value
    elif direction == "forward":
        currentPosition[0] += value

print("Part 1", currentPosition, currentPosition[0] * currentPosition[1])

# Part 2

currentPosition = [0, 0, 0]  # x, z, aim

for (direction, value) in instructions:
    if direction == "up":
        currentPosition[2] -= value
    elif direction == "down":
        currentPosition[2] += value
    elif direction == "forward":
        currentPosition[0] += value
        currentPosition[1] += currentPosition[2] * value

    # debug
    # print(direction, value, "=>", currentPosition)

print("Part 2", currentPosition, currentPosition[0] * currentPosition[1])
