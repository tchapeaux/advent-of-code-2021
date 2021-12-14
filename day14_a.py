import aoc

data = aoc.getLinesForDay(14)

start = None
rules = {}

for idx, line in enumerate(data):
    if idx == 0:
        start = line
    elif "->" in line:
        rule = tuple(line.split(" -> "))
        rules[rule[0]] = rule[1]

current = start

for step in range(10):
    # Construct the new iteration char by char
    newPolymer = current[0]
    for idx, char in enumerate(current):
        if idx == 0:
            continue
        pair = current[idx - 1] + char
        if pair in rules:
            newPolymer += rules[pair] + char
        else:
            newPolymer += char
    current = newPolymer

final = current

# Count elements
count_elems = {}
for char in final:
    if char not in count_elems:
        count_elems[char] = 0
    count_elems[char] += 1

print("Part 1", max(count_elems.values()) - min(count_elems.values()))