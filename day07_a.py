import aoc

data = aoc.getInputForDay(7)

# example
# data = "16,1,2,0,4,2,7,1,2,14"

# print(data)

crabs = [int(x) for x in data.split(",")]

minCrab = min(crabs)
maxCrab = max(crabs)


currentWinner = None
currentMinimalFuel = (maxCrab - minCrab) * 100000
for candidate in range(minCrab, maxCrab + 1):
    fuel = sum([abs(crab - candidate) for crab in crabs])
    if fuel < currentMinimalFuel:
        currentWinner = candidate
        currentMinimalFuel = fuel

print("Part 1", currentWinner, currentMinimalFuel)

# Pre-compute all fuel costs per distance
fuelCosts = []
for distance in range(maxCrab - minCrab + 10):
    if len(fuelCosts) == 0:
        fuelCosts.append(0)
    else:
        fuelCosts.append(fuelCosts[distance - 1] + distance)


currentWinner = None
currentMinimalFuel = fuelCosts[-1] * 100

for candidate in range(minCrab, maxCrab + 1):
    fuel = sum([fuelCosts[abs(crab - candidate)] for crab in crabs])
    if fuel < currentMinimalFuel:
        currentWinner = candidate
        currentMinimalFuel = fuel

print("Part 2", currentWinner, currentMinimalFuel)


# 99274102 your answer is too high
