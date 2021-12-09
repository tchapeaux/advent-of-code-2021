import aoc

data = aoc.getLinesForDay(8)
# data = aoc.getLinesForDay(8, force_filepath="inputs/day08_example.txt")


displays = [[set(list(s)) for s in d.split(" | ")[0].split(" ")] for d in data]
outputs = [[set(list(s)) for s in d.split(" | ")[1].split(" ")] for d in data]

DIGITS = list(range(10))
SEGMENTS = list("abcdefg")

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


# Part 2 -- decode every segment

outputSum = 0
for patterns, output in zip(displays, outputs):
    print("")
    # We need to find the whole bijection A --> B

    # When a pattern has been associated to a digit, map it here
    patt_for_1 = [p for p in patterns if len(p) == 2][0]
    patt_for_7 = [p for p in patterns if len(p) == 3][0]
    patt_for_4 = [p for p in patterns if len(p) == 4][0]
    patt_for_8 = [p for p in patterns if len(p) == 7][0]

    bijection = {}

    """
    Visual representation of the segments
    (this helps follow the code)
    (number at the start is the segment size)

    7 abcdefg

    6 abcd fg
    6 abc efg
    6 ab defg

    5 ab d fg
    5 a cde g
    5 a cd fg

    4  bcd f

    3 a c  f

    2   c  f
    """

    # Hardcode the deduction steps
    # find a by comparing 1 (cf) and 7 (acf)
    a = [c for c in patt_for_7 if c not in patt_for_1][0]
    # this gives us two candidates for c & f...
    c_f = [c for c in patt_for_7 if c in patt_for_1]
    # ...which we can differentiate by looking at the 3 patterns of size 6 (all have f, 2 have c)
    patt6 = [_p for _p in patterns if len(_p) == 6]
    f = [x for x in c_f if all([x in _p for _p in patt6])][0]
    c = [x for x in c_f if x != f][0]
    # g is the segment in all patterns of len>=5 and in none of len<5
    pattSmaller5 = [_p for _p in patterns if len(_p) < 5]
    g = [
        s
        for s in SEGMENTS
        if all([s not in _p for _p in patterns if _p in pattSmaller5])
        and all([s in _p for _p in patterns if _p not in pattSmaller5])
    ][0]
    # remaining: b, d, e
    e_d_b = [s for s in SEGMENTS if s not in [a, c, f, g]]
    # b is the only one in all segments of size 6
    b = [x for x in e_d_b if all([x in _p for _p in patt6])][0]
    # d is the only one in all segments of size 5
    patt5 = [_p for _p in patterns if len(_p) == 5]
    d = [x for x in e_d_b if x != b and all([x in _p for _p in patt5])][0]
    # e is the last one
    e = [x for x in e_d_b if x != d and x != b][0]
    bijection["a"] = a
    bijection["b"] = b
    bijection["c"] = c
    bijection["d"] = d
    bijection["e"] = e
    bijection["f"] = f
    bijection["g"] = g

    for s in bijection.keys():
        print(s, bijection[s])

    # Find the new digits mapping using the bijection
    newDigitMapping = [None for _ in DIGITS]
    for digit in DIGITS:
        targetPattern = set([bijection[d] for d in DIGIT_MAPPING[digit]])
        assert targetPattern in patterns
        newDigitMapping[digit] = targetPattern

    # Decode the output
    assert len(output) == 4
    outputValue = (
        1000 * newDigitMapping.index(output[0])
        + 100 * newDigitMapping.index(output[1])
        + 10 * newDigitMapping.index(output[2])
        + newDigitMapping.index(output[3])
    )
    outputSum += outputValue

print("Part 2", outputSum)

# 61229 too low -- was actually the example output (oops)