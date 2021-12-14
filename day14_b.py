from collections import defaultdict

import aoc

data = aoc.getLinesForDay(14)
# data = aoc.getLinesForDay(14, force_filepath="inputs/day14_example.txt")

start = None
rules = {}

for idx, line in enumerate(data):
    if idx == 0:
        start = line
    elif "->" in line:
        rule = tuple(line.split(" -> "))
        rules[rule[0]] = rule[1]


firstChar = start[0]
endChar = start[-1]

currentPairCount = {}
for idx in range(len(start) - 1):
    pair = start[idx] + start[idx + 1]
    if pair not in currentPairCount:
        currentPairCount[pair] = 0
    currentPairCount[pair] += 1

print("Template", currentPairCount)

for step in range(40):
    newCurrentPairCount = defaultdict(int)
    for pair in currentPairCount:
        count = currentPairCount[pair]
        if pair in rules:
            newChar = rules[pair]
            newCurrentPairCount[pair[0] + newChar] += count
            newCurrentPairCount[newChar + pair[1]] += count
        else:
            newCurrentPairCount[pair] = count
    currentPairCount = newCurrentPairCount
    print("Step", step + 1, currentPairCount)

finalPairCount = currentPairCount

# Count elements
count_elems = {}
for pair, value in finalPairCount.items():
    leftChar = pair[0]
    rightChar = pair[1]

    if leftChar not in count_elems:
        count_elems[leftChar] = 0
    if rightChar not in count_elems:
        count_elems[rightChar] = 0

    # We divide by 2 because each char will be counted twice (as leftChar and rightChar)
    count_elems[leftChar] += value / 2
    count_elems[rightChar] += value / 2

# We add the firstChar and lastChar because we half-counted them on the step above
count_elems[firstChar] += 0.5
count_elems[endChar] += 0.5

print(
    "Part 2",
    int(max(count_elems.values())),
    "-",
    int(min(count_elems.values())),
    "=",
    int(max(count_elems.values()) - min(count_elems.values())),
)


# 4807056953864 too low -- I think this is a OBO error
# 4807056953865 too low -- guess not :/
# 4807056953866 was right.... so it was a OBT (Off By Two) this time 😂