import aoc

data = aoc.getLinesForDay(21)


player1Position = int(data[0][-1])
player2Position = int(data[1][-1])

# Example
# player1Position = 4
# player2Position = 8

score1 = 0
score2 = 0

players = [
    {"pos": player1Position, "score": score1},
    {"pos": player2Position, "score": score2},
]

MAX_SCORE = 1000

currentDiceValue = 0
diceCnt = 0


def getNextDiceValue():
    global currentDiceValue
    global diceCnt
    nextValue = currentDiceValue + 1
    if nextValue > 100:
        nextValue = 1
    currentDiceValue = nextValue
    diceCnt += 1
    return nextValue


step = 0
while all([p["score"] < MAX_SCORE for p in players]):
    step += 1
    print("Step", step)
    print("State", players)
    # Player 1 turn
    for _ in range(3):
        dice = getNextDiceValue()
        players[0]["pos"] += dice
        while players[0]["pos"] > 10:
            players[0]["pos"] -= 10
    players[0]["score"] += players[0]["pos"]

    if players[0]["score"] >= MAX_SCORE:
        break

    # Player 2 turn
    for _ in range(3):
        dice = getNextDiceValue()
        players[1]["pos"] += dice
        while players[1]["pos"] > 10:
            players[1]["pos"] -= 10
    players[1]["score"] += players[1]["pos"]

print("Final state", players, "steps", step, "dice cnt", diceCnt)

print("Part 1", min(p["score"] for p in players) * diceCnt)