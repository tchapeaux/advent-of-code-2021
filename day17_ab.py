import aoc


def reachesTarget(initialSpeed, targetDimensions):
    xMin, xMax, yMin, yMax = targetDimensions
    xSpeed, ySpeed = initialSpeed

    assert xMin < xMax
    assert yMin < yMax

    currentX, currentY = 0, 0
    maxObservedY = 0

    while True:
        # Move probe
        currentX += xSpeed
        currentY += ySpeed

        # Check for new record
        if currentY > maxObservedY:
            maxObservedY = currentY

        # Apply drag
        if xSpeed > 0:
            xSpeed -= 1
        ySpeed -= 1

        if xMin <= currentX <= xMax and yMin <= currentY <= yMax:
            return True, maxObservedY

        if currentY < yMin and ySpeed < 0:
            return False, maxObservedY
        if currentX > xMax:
            return False, maxObservedY


data = aoc.getInputForDay(17)
# data = "target area: x=20..30, y=-10..-5"


data = data.replace("target area: ", "")


xData, yData = data.split(", ")
targetXMin, targetXMax = (int(val) for val in xData[2:].split(".."))
targetYMin, targetYMax = (int(val) for val in yData[2:].split(".."))


targetDimensions = (targetXMin, targetXMax, targetYMin, targetYMax)

# Examples
exampleTargetDimentions = (20, 30, -10, -5)
assert reachesTarget((7, 2), exampleTargetDimentions) == (True, 3)
assert reachesTarget((6, 3), exampleTargetDimentions) == (True, 6)
assert reachesTarget((9, 0), exampleTargetDimentions) == (True, 0)
assert reachesTarget((17, -4), exampleTargetDimentions) == (False, 0)

maxObservedMaxY = 0
reachesCount = 0
for ySpeed in range(targetYMin, 100):
    for xSpeed in range(0, targetXMax + 1):
        initialSpeed = (xSpeed, ySpeed)
        hasReached, yMax = reachesTarget((xSpeed, ySpeed), targetDimensions)
        if hasReached:
            print("reaches?", xSpeed, ySpeed, "=>", hasReached, yMax)
            reachesCount += 1
            if yMax > maxObservedMaxY:
                maxObservedMaxY = yMax

print("Part 1", maxObservedMaxY)
print("Part 2", reachesCount)

# 656 too low -- used targetYMax instead of targetYMin for lower bound for the exhaustive search