import aoc

data = [int(x) for x in aoc.getLinesForDay(1)]

# Example data
""""
data = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]
"""

acc = 0
for idx, depth in enumerate(data):
    if idx == 0:
        continue
    if depth > data[idx - 1]:
        acc += 1

print("part 1", acc)

# 1680 too low --- forgot to use int()

acc2 = 0
lastSum = 100000000  # or maxInt or whatever

for idx, _ in enumerate(data):
    if idx >= len(data) - 2:
        continue

    thisSum = data[idx] + data[idx + 1] + data[idx + 2]
    if thisSum > lastSum:
        acc2 += 1

    lastSum = thisSum

print("part 2", acc2)

# 3384 too high -- re-used the old acc variable by accident
# 1703 too low -- continue condition was wrong in the loop, so I stopped too early