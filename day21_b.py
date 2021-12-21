from collections import Counter
from copy import deepcopy

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

MAX_SCORE = 21

running_universes = Counter()
# running_universes will have the following tuple as key
# (player1Pos, player1Score, player2Pos, player2Score, nextPlayerIdx)
running_universes[
    (players[0]["pos"], players[0]["score"], players[1]["pos"], players[1]["score"], 0)
] = 1

stopped_universes = Counter()


# For each player, we do 3 dice rolls, so 3 * 3 * 3 universes are created
# However, some of them have the exact same result
# We pre-compute this here
threeDiceRollsUniverses = Counter()
for d1 in [1, 2, 3]:
    for d2 in [1, 2, 3]:
        for d3 in [1, 2, 3]:
            threeDiceRollsUniverses[d1 + d2 + d3] += 1


def getNewState(players, playerTurn, threeDiceValue):
    newPlayers = deepcopy(players)
    p = newPlayers[playerTurn]
    p["pos"] += threeDiceValue
    while p["pos"] > 10:
        p["pos"] -= 10
    p["score"] += p["pos"]
    return newPlayers


step = 0
while len(running_universes) > 0:
    step += 1
    print("Simulating all step", step)
    nextStepUniverses = Counter()
    for state in running_universes:
        stateCount = running_universes[state]
        players = [
            {"pos": state[0], "score": state[1]},
            {"pos": state[2], "score": state[3]},
        ]
        playerTurn = state[4]

        for possibleScore in threeDiceRollsUniverses:
            occurences = threeDiceRollsUniverses[possibleScore]

            newState = getNewState(players, playerTurn, possibleScore)

            newStateAsKey = (
                newState[0]["pos"],
                newState[0]["score"],
                newState[1]["pos"],
                newState[1]["score"],
                (playerTurn + 1) % 2,
            )

            if newState[0]["score"] >= MAX_SCORE or newState[1]["score"] >= MAX_SCORE:
                stopped_universes[newStateAsKey] += occurences * stateCount
            else:
                nextStepUniverses[newStateAsKey] += occurences * stateCount

    running_universes = nextStepUniverses

print("== all stopped")

player1UniversesWon = 0
player2UniversesWon = 0
for univ in stopped_universes:
    occurences = stopped_universes[univ]
    if univ[1] >= 21:
        player1UniversesWon += occurences
    else:
        assert univ[3] >= 21
        player2UniversesWon += occurences

print(max([player1UniversesWon, player2Position]))