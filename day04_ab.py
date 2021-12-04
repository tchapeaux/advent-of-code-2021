import aoc

import re

lines = aoc.getLinesForDay(4)
# lines = aoc.getLinesForDay(4, force_filepath="inputs/day4_example.txt")

drawnNumbers = [int(num) for num in lines[0].split(",")]
boards = []

currentBoard = None
for line in lines[1:]:
    if len(line.strip()) == 0:
        if currentBoard:
            boards.append(currentBoard)
        currentBoard = []
    else:
        row = re.split(r"\s+", line)
        currentBoard.append([int(x) for x in row])

if len(currentBoard) > 0:
    boards.append(currentBoard)

""" what we want
marks = [
    [(1, 2), (2, 1), ]  # board 0 marks
    etc
]
"""


def boardHasWon(marksInBoard):
    for x in range(5):
        if all([(y, x) in marksInBoard for y in range(5)]):
            return True

    for y in range(5):
        if all([(y, x) in marksInBoard for x in range(5)]):
            return True

    return False


def getWinValue(board, marksForBoard, drawnNum):
    sumUnmarked = 0
    for y in range(5):
        for x in range(5):
            if (x, y) not in marksForBoard:
                sumUnmarked += board[y][x]

    return sumUnmarked * drawnNum


def searchWinningBoard():
    marks = [[] for b in boards]
    for drawnNumb in drawnNumbers:
        print("Drawn", drawnNumb)
        for boardIdx, b in enumerate(boards):
            for y in range(len(b)):
                for x in range(len(b[y])):
                    num = b[y][x]
                    if num == drawnNumb:
                        marks[boardIdx].append((x, y))
                        if boardHasWon(marks[boardIdx]):
                            return getWinValue(b, marks[boardIdx], drawnNumb)


print("Part 1", searchWinningBoard())

# 37536 too low


def searchLastWinningBoard():
    marks = [[] for b in boards]
    wonBoards = []
    for drawnNumb in drawnNumbers:
        for boardIdx, b in enumerate(boards):
            if boardIdx in wonBoards:
                continue
            for y in range(len(b)):
                for x in range(len(b[y])):
                    num = b[y][x]
                    if num == drawnNumb:
                        marks[boardIdx].append((x, y))
                        if boardHasWon(marks[boardIdx]):
                            print("BOARD HAS WON", boardIdx)
                            wonBoards.append(boardIdx)
                            if len(wonBoards) == len(boards):
                                return getWinValue(b, marks[boardIdx], drawnNumb)


print("Part 2", searchLastWinningBoard())

# 9471 too high