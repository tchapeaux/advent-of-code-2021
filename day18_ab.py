import aoc
import json
import math
import copy
import time

start_time = time.time()


class SnailSingleNumb(object):
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

    def getMag(self):
        return self.value

    def __repr__(self):
        return f"({self.value})"


class SnailPair(object):
    def __init__(self, initList, parent=None):
        assert len(initList) == 2
        self.parent = parent
        self.left = (
            SnailPair(initList[0], parent=self)
            if isinstance(initList[0], list)
            else SnailSingleNumb(initList[0], self)
        )
        self.right = (
            SnailPair(initList[1], parent=self)
            if isinstance(initList[1], list)
            else SnailSingleNumb(initList[1], self)
        )

    def __repr__(self):
        return f"[{self.left}, {self.right}]"

    def getDepth(self):
        depth = 0
        current = self
        while current.parent is not None:
            depth += 1
            current = current.parent

        return depth

    def getMag(self):
        leftValue = self.left.getMag()
        rightValue = self.right.getMag()
        return 3 * leftValue + 2 * rightValue

    def getDepthFirstPairs(self):
        if isinstance(self.left, SnailPair):
            leftPairs = list(self.left.getDepthFirstPairs())
            for pair in leftPairs:
                yield pair

        yield self

        if isinstance(self.right, SnailPair):
            rightPairs = list(self.right.getDepthFirstPairs())
            for pair in rightPairs:
                yield pair

    def getDepthFirstNumbers(self):
        for pair in self.getDepthFirstPairs():
            if isinstance(pair.left, SnailSingleNumb):
                yield pair.left
            if isinstance(pair.right, SnailSingleNumb):
                yield pair.right

    def reduce(self):
        didExplode, didSplit = True, True
        while didExplode or didSplit:
            didExplode, didSplit = False, False
            # print("reduce?", self)

            for pair in self.getDepthFirstPairs():
                if pair.getDepth() >= 4:
                    # print("EXPLODE!", pair)
                    # EXPLODE

                    # get ordered all values in the current number
                    root = self
                    while self.parent is not None:
                        root = self.parent
                    allValues = list(root.getDepthFirstNumbers())

                    # Find value directly to the left of the pair
                    leftValue = pair.left
                    for valueIdx, value in enumerate(allValues):
                        if value is leftValue and valueIdx > 0:
                            # Add pair left value to target value
                            targetValue = allValues[valueIdx - 1]
                            targetValue.value += leftValue.value
                    # Find value directly to the right of the pair
                    rightValue = pair.right
                    for valueIdx, value in enumerate(allValues):
                        if value is rightValue and valueIdx < len(allValues) - 1:
                            # Add pair right value to target value
                            targetValue = allValues[valueIdx + 1]
                            targetValue.value += rightValue.value

                    # Replace pair by 0
                    parent = pair.parent
                    if pair is parent.left:
                        parent.left = SnailSingleNumb(0, parent)
                    else:
                        assert pair is parent.right
                        parent.right = SnailSingleNumb(0, parent)

                    # Mark pair as exploded and stop there
                    didExplode = True
                    break

            if not didExplode:
                for numb in self.getDepthFirstNumbers():
                    if numb.value >= 10:
                        # SPLIT
                        # print("SPLIT!", numb)
                        left = math.floor(numb.value / 2)
                        right = math.ceil(numb.value / 2)
                        newPair = SnailPair([left, right], parent=numb.parent)
                        if numb is numb.parent.left:
                            numb.parent.left = newPair
                        else:
                            assert numb.parent.right == numb
                            numb.parent.right = newPair

                        didSplit = True
                        break

    def __add__(self, anotherPair):
        assert self.parent is None, "Cannot add a child pair"
        assert anotherPair.parent is None, "Cannot add a child pair"
        newPair = SnailPair([0, 0])
        newPair.left = copy.deepcopy(self)
        newPair.right = copy.deepcopy(anotherPair)
        newPair.left.parent = newPair
        newPair.right.parent = newPair
        return newPair


data = aoc.getLinesForDay(18)
# data = aoc.getLinesForDay(18, force_filepath="inputs/day18_part_b_example.txt")

print(data)

originalNumbers = []
for line in data:
    originalNumbers.append(SnailPair(json.loads(line)))
    print(originalNumbers[-1], list(originalNumbers[-1].getDepthFirstNumbers()))

print("Try to reduce")
EXAMPLE_REDUCE = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
s = SnailPair(json.loads(EXAMPLE_REDUCE))
s.reduce()
print(s)


def testMag(pairStr, expectedVal):
    s = SnailPair(json.loads(pairStr))
    assert s.getMag() == expectedVal, s.getMag()


testMag("[[1,2],[[3,4],5]]", 143)

# Using deepcopy because it turns out my algo breaks the original list (oops)
numbers = copy.deepcopy(originalNumbers)

acc = numbers[0]
for idx, next in enumerate(numbers[1:]):
    print("add", idx, "/", len(numbers))
    acc = acc + next
    acc.reduce()

print("Part 1", acc.getMag())

# 95 not the right answer -- forgot that magnitude was 3A + 2B instead of A + B

# Part 2 - let's not kid ourselves, we will brute force it
numbers = copy.deepcopy(originalNumbers)
bestMag = 0
for idxA, numberA in enumerate(numbers):
    for idxB, numberB in enumerate(numbers):
        if numberA is numberB:
            continue
        theSum = numberA + numberB
        theSum.reduce()
        theMag = theSum.getMag()
        print(idxA, "+", idxB, "=", theMag)
        if theMag > bestMag:
            bestMag = theMag
            print("New bestMag")

print("Part 2", bestMag)

# 13494 too high -- forgot to reduce() the sum

print("it only took", time.time() - start_time, "seconds")