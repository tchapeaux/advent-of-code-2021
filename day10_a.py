import math

import aoc

data = aoc.getLinesForDay(10)
# data = aoc.getLinesForDay(10, force_filepath="inputs/day10_example.txt")

CHUNKS_PAIRS = [("(", ")", 3), ("[", "]", 57), ("{", "}", 1197), ("<", ">", 25137)]

OPEN_CHARS = [p[0] for p in CHUNKS_PAIRS]
CLOSE_CHARS = [p[1] for p in CHUNKS_PAIRS]


def getCloseCharFor(openChar):
    assert openChar in OPEN_CHARS
    pair = [p for p in CHUNKS_PAIRS if p[0] == openChar][0]
    return pair[1]


def isValidPair(openChar, closeChar):
    assert openChar in OPEN_CHARS and closeChar in CLOSE_CHARS
    validCloseChar = getCloseCharFor(openChar)
    return closeChar == validCloseChar


def scoreOf(invalidClose):
    assert invalidClose in CLOSE_CHARS
    pair = [p for p in CHUNKS_PAIRS if p[1] == invalidClose][0]
    return pair[2]


# For part 2
AUTOCOMPLETE_SCORES = [(")", 1), ("]", 2), ("}", 3), (">", 4)]

autocompleteScoresPerLine = []

myScore = 0
for lineIdx, line in enumerate(data):
    myStack = []
    corruptedFlag = False
    for charIdx, char in enumerate(line):
        if char in OPEN_CHARS:
            myStack.append(char)
        elif char in CLOSE_CHARS:
            correspondingOpen = myStack[-1]
            if not isValidPair(correspondingOpen, char):
                score = scoreOf(char)
                print("Line", lineIdx, "invalid", char, "at char", charIdx, "=>", score)
                myScore += score
                corruptedFlag = True
                break
            else:
                myStack.pop()
    else:
        print("Line", lineIdx, "not corrupted")
    if len(myStack) > 0 and not corruptedFlag:
        lineAutoCompleteScore = 0
        for openChar in myStack[::-1]:
            closeChar = getCloseCharFor(openChar)
            lineAutoCompleteScore *= 5
            scoreForCloseChar = [s for s in AUTOCOMPLETE_SCORES if s[0] == closeChar][0]
            lineAutoCompleteScore += scoreForCloseChar[1]
        print("...however incomplete with score", lineAutoCompleteScore)
        autocompleteScoresPerLine.append(lineAutoCompleteScore)


print("Part 1 -- syntax error score", myScore)

# 10639428 too high -- forgot to break out of the loop so was counting every corruption
# 485412 too high -- forgot to pop in my stack so every pair after the first was corrupted

autocompleteScoresPerLine = sorted(autocompleteScoresPerLine)
numberOfIncompleteLines = len(autocompleteScoresPerLine)
print(
    "Part 2 -- autocomplete score",
    autocompleteScoresPerLine[math.floor(numberOfIncompleteLines / 2)],
)

# 1091319617 too low -- was counting autocomplete score for corrupted lines as well