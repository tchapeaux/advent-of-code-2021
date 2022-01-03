# Playground file
# This is just for small experiments during the jam
# Mostly useful for me when I forget what the exact Python syntax for something is

import aoc
import re


a = set("abcd")
b = set(["a", "b", "c", "d"])
print(a is b)

a = (1, 2)
b = (1, 3)

print(a is not b)

print([1, 2, 3, 4][2:])

a = "1234567890abcdefgh"

d = "tch"

e, d = (1, 2)
print(d)

a = (1, 65)
b = (3, 12)
print(a + b)


for d in range(1, 10):
    print(d, ((d + 10) % 26) - 11)