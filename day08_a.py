import aoc

data = aoc.getLinesForDay(8)
# data = aoc.getLinesForDay(8, force_filepath="inputs/day08_example.txt")

# print(data)


def sortStr(s):
    """ return a new string with the same letters in alphabetical order """
    return "".join(sorted([c for c in s]))


displays = [[sortStr(s) for s in d.split(" | ")[0].split(" ")] for d in data]
outputs = [[sortStr(s) for s in d.split(" | ")[1].split(" ")] for d in data]

# Which segments are needed for each digit in the baseline case
DIGIT_MAPPING = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bcdf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]

# Part 1 -- simply find 1, 4, 7 and 8

count_occurences = 0

for patterns, output in zip(displays, outputs):
    print("")
    print("patterns", patterns)
    patt_1 = [p for p in patterns if len(p) == 2][0]
    patt_7 = [p for p in patterns if len(p) == 3][0]
    patt_4 = [p for p in patterns if len(p) == 4][0]
    patt_8 = [p for p in patterns if len(p) == 7][0]

    patterns_to_match = [patt_1, patt_7, patt_4, patt_8]
    print("to match", patterns_to_match)
    print("output", output)
    matching_output = [o for o in output if o in patterns_to_match]
    print("matched", matching_output)
    count_occurences += len(matching_output)

print(count_occurences)

# 69 not the right answer because I forgot to sort (so cg !== gc)
