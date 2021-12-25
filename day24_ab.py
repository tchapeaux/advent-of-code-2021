import math
import random

import aoc

data = aoc.getLinesForDay(24)
dataOpti = aoc.getLinesForDay(24, force_filepath="inputs/day24_cleaned.txt")


class ALU(object):
    def __init__(self, program, inputs):
        self.variables = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }

        self.currentInstr = 0

        self.program = program
        self.inputs = inputs

        self.zValueAtEachInp = []

    def execute(self, line):
        # parse line
        (instr, *args) = line.split(" ")
        if instr == "inp":
            [
                var,
            ] = args
            self.variables[var] = int(self.inputs.pop(0))
            self.zValueAtEachInp.append(self.variables["z"])
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
        if instr == "set":
            self.variables[var1] = val2

    def run(self):
        assert self.currentInstr == 0, "Already run!"
        for line in self.program:
            # print(line)
            self.execute(line)
            # print(self.variables)

        return self.variables


def getIntermediateResult(testNumber, stepNumber):
    xAsStr = str(testNumber)
    assert len(xAsStr) == 14, (len(xAsStr), xAsStr)
    assert "0" not in xAsStr

    alu = ALU(data, [c for c in xAsStr])
    alu.run()

    return alu.zValueAtEachInp[stepNumber]


def comparePrograms(testNumber):
    xAsStr = str(testNumber)
    assert len(xAsStr) == 14, (len(xAsStr), xAsStr)
    assert "0" not in xAsStr

    alu = ALU(data, [c for c in xAsStr])
    alu.run()

    aluOpti = ALU(dataOpti, [c for c in xAsStr])
    aluOpti.run()

    print(alu.variables["z"])
    assert alu.variables["z"] == aluOpti.variables["z"]


comparePrograms(12345678912312)

for _ in range(500):
    testNbr = "".join([str(math.floor(random.random() * 9) + 1) for _ in range(14)])
    print(testNbr)
    comparePrograms(testNbr)