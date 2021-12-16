import aoc

# For some reason the leading zero make the bin() function mess up my logic
# (only happen for the long input and not for the examples)
# => let's use a custom map
HEX_TO_BIN_MAP = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hexToBin(hexString):
    return "".join([HEX_TO_BIN_MAP[hx] for hx in hexString.strip()])


def binToDec(binString):
    return int(binString, 2)


class Packet(object):
    def __init__(self):
        self.version = None
        self.type = None
        self.lengthTypeId = None
        self.length = None
        self.literalValue = None
        self.subPackets = None


LITERAL = 4

LENGTH_TOTAL_SIZE = 0
LENGTH_NB_OF_SUB = 1

MINIMAL_PACKET_SIZE = 6


def parsePackets(inputStr):
    packetsAndSubpackets = []

    def readOnePacket(inputStr, currentPos):
        # Read one packet then return the packet and the new position
        # currentPos must be at the start of a packet (or subpacket)

        # print("== new packet")
        # print("current pos", currentPos)
        # print("remaining: ", len(inputStr) - currentPos)

        assert currentPos + MINIMAL_PACKET_SIZE < len(inputStr)

        current = Packet()
        current.version = binToDec(inputStr[currentPos : currentPos + 3])
        currentPos += 3
        # print("version", current.version)
        current.type = binToDec(inputStr[currentPos : currentPos + 3])
        currentPos += 3
        # print("type", current.type)
        if current.type == LITERAL:
            accData = ""

            while True:
                firstBit = inputStr[currentPos]
                currentPos += 1

                accData += inputStr[currentPos : currentPos + 4]
                currentPos += 4

                if firstBit != "1":
                    break

            current.literalValue = binToDec(accData)
            # print("literal value", current.literalValue)

        elif current.type != LITERAL:
            # if not literal -> operator
            current.lengthTypeId = int(inputStr[currentPos])
            currentPos += 1

            current.subPackets = []
            if current.lengthTypeId == LENGTH_TOTAL_SIZE:
                # print("length type: total size")
                current.length = binToDec(inputStr[currentPos : currentPos + 15])
                currentPos += 15
                # print("length", current.length)
                assert current.length > 0
                targetCurrentPos = currentPos + current.length
                while currentPos != targetCurrentPos:
                    assert currentPos < targetCurrentPos
                    """
                    print(
                        "searching for subpacket....",
                        currentPos,
                        "of",
                        targetCurrentPos,
                        "bits",
                    )
                    """
                    newPacket, currentPos = readOnePacket(inputStr, currentPos)
                    current.subPackets.append(newPacket)
                # print(f"% got all {current.length} bits")
            elif current.lengthTypeId == LENGTH_NB_OF_SUB:
                # print("length type: nb of subpackets")
                # print(inputStr[currentPos : currentPos + 11])
                current.length = binToDec(inputStr[currentPos : currentPos + 11])
                currentPos += 11
                # print("length", current.length)
                assert current.length > 0
                while len(current.subPackets) < current.length:
                    """
                    print(
                        "searching for subpacket....",
                        len(current.subPackets),
                        "of",
                        current.length,
                        "packets",
                    )
                    """
                    newPacket, currentPos = readOnePacket(inputStr, currentPos)
                    current.subPackets.append(newPacket)
                # print(f"% got all {current.length} packets")
            else:
                raise Exception("Unknown lengthTypeId", current.lengthTypeId)
        else:
            raise Exception("Unknown packet type ", current.type)

        packetsAndSubpackets.append(current)
        return current, currentPos

    currentPos = 0
    while currentPos < len(inputStr) - MINIMAL_PACKET_SIZE - 1:
        _, currentPos = readOnePacket(inputStr, currentPos)

    # print("Found", len(packetsAndSubpackets), "packets")
    return packetsAndSubpackets


def getVersionSum(packets):
    versionSum = sum([p.version for p in packets])
    return versionSum


data = aoc.getInputForDay(16)
# data = aoc.getInputForDay(16, force_filepath="inputs/day16_cropped.txt")


binData = hexToBin(data)
assert getVersionSum(parsePackets(hexToBin("D2FE28"))) == 6
assert getVersionSum(parsePackets(hexToBin("38006F4529120"))) == 9
assert getVersionSum(parsePackets(hexToBin("8A004A801A8002F478"))) == 16
assert getVersionSum(parsePackets(hexToBin("620080001611562C8802118E34"))) == 12
assert getVersionSum(parsePackets(hexToBin("C0015000016115A2E0802F182340"))) == 23
assert getVersionSum(parsePackets(hexToBin("A0016C880162017C3686B18A3D4780"))) == 31

inputPackets = parsePackets(binData)
print("Part 1", getVersionSum(inputPackets))


# 960 too low (hard to debug issue with the zero-padding of the binary)

# For Part 2, we need to compute the packets value

SUM = 0
PRODUCT = 1
MIN = 2
MAX = 3
GT = 5
LT = 6
EQ = 7


def getPacketValue(packet):
    if packet.type == LITERAL:
        return packet.literalValue

    subValues = [getPacketValue(p) for p in packet.subPackets]

    if packet.type == SUM:
        return sum(subValues)

    if packet.type == PRODUCT:
        acc = 1
        for v in subValues:
            acc *= v
        return acc

    if packet.type == MIN:
        return min(subValues)

    if packet.type == MAX:
        return max(subValues)

    if packet.type == GT:
        assert len(packet.subPackets) == 2
        return 1 if subValues[0] > subValues[1] else 0

    if packet.type == LT:
        assert len(packet.subPackets) == 2
        return 1 if subValues[0] < subValues[1] else 0

    if packet.type == EQ:
        assert len(packet.subPackets) == 2
        return 1 if subValues[0] == subValues[1] else 0


# I guess the outermost packet is the last added packet? (this should make sense)


assert getPacketValue(parsePackets(hexToBin("C200B40A82"))[-1]) == 3
assert getPacketValue(parsePackets(hexToBin("04005AC33890"))[-1]) == 54
assert getPacketValue(parsePackets(hexToBin("880086C3E88112"))[-1]) == 7
assert getPacketValue(parsePackets(hexToBin("CE00C43D881120"))[-1]) == 9
assert getPacketValue(parsePackets(hexToBin("D8005AC2A8F0"))[-1]) == 1
assert getPacketValue(parsePackets(hexToBin("F600BC2D8F"))[-1]) == 0
assert getPacketValue(parsePackets(hexToBin("9C005AC2F8F0"))[-1]) == 0
assert getPacketValue(parsePackets(hexToBin("9C0141080250320F1802104A08"))[-1]) == 1


print("Part 2", getPacketValue(inputPackets[-1]))

# 2223948314877 too high (forgot to change my copy-paste for EQ)