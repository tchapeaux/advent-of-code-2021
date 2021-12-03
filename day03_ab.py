import aoc

# data = aoc.getCellsInput(3, force_filepath="inputs/day3_example.txt")
data = aoc.getCellsInput(3)

# This code is ugly
# Leaving it in all its messy glory because that is the AoC way

print("\n".join(["".join(row) for row in data]))

gamma = []
epsilon = []

oxygen_candidates = [row for row in data]
co2_candidates = [row for row in data]

oxygen_final_row = None
co2_final_row = None


def countValues(row, val):
    return len([1 for cell in row if cell == val])


for bitPos in range(len(data[0])):
    print("=== bitpos", bitPos)

    numberOfOnes = countValues([row[bitPos] for row in data], "1")
    numberOfZeroes = countValues([row[bitPos] for row in data], "0")

    print("number of ones", numberOfOnes)
    print("number of zeroes", numberOfZeroes)

    gamma.append(1 if numberOfOnes > numberOfZeroes else 0)
    epsilon.append(0 if numberOfOnes > numberOfZeroes else 1)

    if len(oxygen_candidates) > 1:
        numberOfOnesInCandidates = countValues(
            [row[bitPos] for row in oxygen_candidates], "1"
        )
        numberOfZeroesInCandidates = countValues(
            [row[bitPos] for row in oxygen_candidates], "0"
        )
        mostCommonOxygenValue = (
            1 if numberOfOnesInCandidates >= numberOfZeroesInCandidates else 0
        )
        print("pos", bitPos, "should be", mostCommonOxygenValue)
        oxygen_candidates = [
            row
            for row in oxygen_candidates
            if int(row[bitPos]) == mostCommonOxygenValue
        ]
    print("oxy", len(oxygen_candidates), oxygen_candidates)
    if len(oxygen_candidates) == 1:
        oxygen_final_row = oxygen_candidates[0]

    if len(co2_candidates) > 1:
        numberOfOnesInCandidates = countValues(
            [row[bitPos] for row in co2_candidates], "1"
        )
        numberOfZeroesInCandidates = countValues(
            [row[bitPos] for row in co2_candidates], "0"
        )
        mostCommonCo2Value = (
            1 if numberOfOnesInCandidates >= numberOfZeroesInCandidates else 0
        )
        co2_candidates = [
            row for row in co2_candidates if int(row[bitPos]) != mostCommonCo2Value
        ]
    print("co2", len(co2_candidates))
    if len(co2_candidates) == 1:
        co2_final_row = co2_candidates[0]


def binToDec(bits):
    size = len(bits)
    acc = 0
    for pos in range((size) - 1, -1, -1):
        acc += int(bits[pos]) * (2 ** (size - 1 - pos))
    return acc


print("gamma", gamma)
print(binToDec(gamma))
print("epsilon", epsilon)
print(binToDec(epsilon))

print("number of rows", len(data))
print("row size", len(data[0]))

print("Part 1", binToDec(gamma) * binToDec(epsilon))

# 1471406 too low

print("oxygen_final_row", (oxygen_final_row))
print("co2_final_row", co2_final_row)

print(
    "Part 2",
    binToDec(oxygen_final_row),
    binToDec(co2_final_row),
    binToDec(oxygen_final_row) * binToDec(co2_final_row),
)

# x one failed attempt as well (don't remember the value)