import math
import random

import aoc

data = aoc.getLinesForDay(24)
dataOpti = aoc.getLinesForDay(24, force_filepath="inputs/day24_cleaned.txt")

COMPARE_PROGRAMS = True


# This is where we validate the list of valid numbers
# the rest of the code is basically what I used to debug + is still used to validate the answers
def getAllPossibleValidNumbers():
    valid = [None for _ in range(14)]

    # Based on reverse engineering on the decompiled code
    # Iterate through the special combinations that create a valid modulo comparison
    # which is the only way to decrease z

    # Note: This is hardcoded for my input

    valid[2] = 9
    valid[3] = 1

    D7_D8 = [(1, 6), (2, 7), (3, 8), (4, 9)]
    for d7, d8 in D7_D8:
        valid[6] = d7
        valid[7] = d8

        D6_D9 = [(8, 1), (9, 2)]
        for d6, d9 in D6_D9:
            valid[5] = d6
            valid[8] = d9

            D10_D11 = [(7, 1), (8, 2), (9, 3)]
            for d10, d11 in D10_D11:
                valid[9] = d10
                valid[10] = d11

                D5_D12 = [(1, 7), (2, 8), (3, 9)]
                for d5, d12 in D5_D12:
                    valid[4] = d5
                    valid[11] = d12

                    D2_D13 = [(x, x - 1) for x in range(2, 10)]
                    for d2, d13 in D2_D13:
                        valid[1] = d2
                        valid[12] = d13

                        D1_D14 = [(x, x + 1) for x in range(1, 9)]
                        for d1, d14 in D1_D14:
                            valid[0] = d1
                            valid[13] = d14

                            yield int("".join([str(d) for d in valid]))


class ALU(object):
    def __init__(self, program, inputs, verbose=False):
        self.variables = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }

        self.program = program
        self.inputs = [int(x) for x in inputs]
        self.verbose = verbose

    def execute(self, line):
        # parse line
        (instr, *args) = line.split(" ")
        if instr == "inp":
            [
                var,
            ] = args
            self.variables[var] = int(self.inputs.pop(0))
            return

        var1, var2 = args
        val2 = self.variables[var2] if var2 in self.variables.keys() else int(var2)

        if instr == "add":
            self.variables[var1] = self.variables[var1] + val2

        if instr == "mul":
            self.variables[var1] = self.variables[var1] * val2

        if instr == "div":
            self.variables[var1] = math.floor(self.variables[var1] / val2)

        if instr == "mod":
            self.variables[var1] = self.variables[var1] % val2

        if instr == "eql":
            self.variables[var1] = 1 if self.variables[var1] == val2 else 0

        # CUSTOM INSTR
        # used by our cleaned up version of the input
        if instr == "set":
            self.variables[var1] = val2

        if instr == "neq":
            self.variables[var1] = 1 if self.variables[var1] != val2 else 0

    def run(self):
        for line in self.program:
            self.execute(line)
            if self.verbose:
                print(line)
                print(self.variables)


if COMPARE_PROGRAMS:

    def getRandom14Digits():
        return int(
            "".join([str(math.floor(random.random() * 9) + 1) for _ in range(14)])
        )

    # Check that our cleanup of the input is equivalent to the initial input
    # by throwing hardcoded + random numbers at it and comparing the results.

    # The cleaned up input was used to generate the hardcoded "valid number" generator above

    def comparePrograms(testNumber):
        xAsStr = str(testNumber)
        assert len(xAsStr) == 14, (len(xAsStr), xAsStr)
        assert "0" not in xAsStr

        alu = ALU(data, [c for c in xAsStr])
        alu.run()

        aluOpti = ALU(dataOpti, [c for c in xAsStr])
        aluOpti.run()

        for var in "wxyz":
            assert alu.variables[var] == aluOpti.variables[var]

    comparePrograms(12345678912312)

    for digit in range(1, 10):
        testNbr = "".join([str(digit) for _ in range(14)])
        comparePrograms(testNbr)

    for _ in range(500):
        testNbr = getRandom14Digits()
        comparePrograms(testNbr)


def isValid(testNumber):
    xAsStr = str(testNumber)
    assert len(xAsStr) == 14, (len(xAsStr), xAsStr)
    assert "0" not in xAsStr

    alu = ALU(data, [c for c in xAsStr], verbose=False)
    alu.run()
    return alu.variables["z"] == 0


validNumbers = list(getAllPossibleValidNumbers())

for validN in validNumbers:
    assert isValid(validN)

print(len(validNumbers), "valid numbers")
print("Part 1", max(validNumbers))
print("Part 2", min(validNumbers))