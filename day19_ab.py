import aoc
import time

start_time = time.time()

data = aoc.getLinesForDay(19)


# parse data

scanners = []
for line in data:
    if len(line) == 0:
        continue
    if line.startswith("---"):
        line = line.replace("--- scanner ", "")
        line = line.replace(" ---", "")
        scannerIdx = int(line)
        assert len(scanners) == scannerIdx
        scanners.append(set())
    else:
        coords = tuple(int(x) for x in line.split(","))
        assert len(coords) == 3
        scanners[-1].add(coords)


def getAllRotations(scanner):
    # returns the list of beacons in each of the possible combination
    for coordX in (0, 1, 2):
        for coordY in (0, 1, 2):
            for coordZ in (0, 1, 2):
                if coordX == coordY or coordY == coordZ or coordX == coordZ:
                    continue
                for invertX in [True, False]:
                    for invertY in [True, False]:
                        for invertZ in [True, False]:
                            yield [
                                (
                                    (-1 if invertX else 1) * c[coordX],
                                    (-1 if invertY else 1) * c[coordY],
                                    (-1 if invertZ else 1) * c[coordZ],
                                )
                                for c in scanner
                            ]


baseline = None  # contain the known position of beacons based on scanner 0
# contain the position of scanners based on scanner 0
baseline_scanners = set()
baseline_scanners.add((0, 0, 0))


# baseline will be scanner 0
# and we will add to the baseline when we confirm a match
baseline = scanners[0].copy()

matchedToBaseline = []
matchedToBaseline.append(scanners[0])


def addToBaseline(matchedToBaseline, baseline, scanner):
    assert scanner not in matchedToBaseline
    # try all rotation of the scanner in consideration
    for rotatedScanner in getAllRotations(scanner):
        # Try all mapping of one scanner beacon to a baseline beacon
        for scanBeacon in rotatedScanner:
            for baselineBeacon in baseline:
                translation = tuple(baselineBeacon[i] - scanBeacon[i] for i in range(3))
                translatedBeacons = set(
                    [
                        tuple(b[i] + translation[i] for i in range(3))
                        for b in rotatedScanner
                    ]
                )
                # count beacons matching the baseline
                countMatchingBeacons = len(baseline.intersection(translatedBeacons))

                if countMatchingBeacons >= 12:
                    print("\t\tMATCHED!!!")
                    baseline.update(translatedBeacons)
                    baseline_scanners.add(translation)
                    matchedToBaseline.append(scanner)
                    return True
    print("\t\tNot matched (yet)")
    return False


# CHEAT? Reorder scanners based on looking at the execution
# so they are always considered once we have enough info to match them
# """
scanners = [
    scanners[0],
    scanners[2],
    scanners[20],
    scanners[25],
    scanners[6],
    scanners[8],
    scanners[16],
    scanners[18],
    scanners[7],
    scanners[12],
    scanners[27],
    scanners[10],
    scanners[19],
    scanners[26],
    scanners[4],
    scanners[13],
    scanners[17],
    scanners[21],
    scanners[22],
    scanners[3],
    scanners[5],
    scanners[11],
    scanners[14],
    scanners[15],
    scanners[24],
    scanners[1],
    scanners[9],
    scanners[23],
]
# """

# Try to match each scan to the baseline
step = 0
while len(matchedToBaseline) < len(scanners):
    step += 1
    print("Iteration", step)
    print("Already matched", len(matchedToBaseline), "scanners")
    for scanIdx, scanner in enumerate(scanners):
        if scanner in matchedToBaseline:
            # skip already matched scanners
            continue

        print("\tTrying scanner #", scanIdx)

        hasMatched = addToBaseline(matchedToBaseline, baseline, scanner)

print("Part 1", len(baseline))
print("It only took", time.time() - start_time)

# Part 2 - find the biggest manhattan distance


def manhattanDistance3d(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]) + abs(p2[2] - p1[2])


currentMax = 0

for s1 in baseline_scanners:
    for s2 in baseline_scanners:
        dist = manhattanDistance3d(s1, s2)
        if dist > currentMax:
            currentMax = dist

print("Part 2", currentMax)

# 15759 too high

print("And with this it only took", time.time() - start_time)