import aoc


data = aoc.getInputForDay(6)

# example
# data = "3,4,3,1,2"

# Part1

fishes = [int(x) for x in data.split(",")]

for day in range(80):
    print(day)
    newFishes = []
    for idx, fish in enumerate(fishes):
        if fish == 0:
            fishes[idx] = 6
            newFishes.append(8)
        else:
            fishes[idx] = fish - 1

    fishes += newFishes

print(len(fishes))
