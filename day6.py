import numpy as np
import math
import sys

lines: list[list[int]] = []
ops = []
part2: dict[int, str] = {}
while True:
    line = sys.stdin.readline().rstrip()
    if line == "":
        print(lines)
        assert False

    split = line.split()
    try:
        lines.append([int(x) for x in split])
    except Exception:
        ops = [sum if x == "+" else math.prod for x in split]
        break

    for i, c in enumerate(line):
        if i not in part2:
            part2[i] = c
        else:
            part2[i] += c

problems = np.array(lines).T
sol1 = sum([op(nums) for op, nums in zip(ops, problems)])

print(f"Solution 1: {sol1}")

it = iter(ops)
sol2 = 0

current: list[int] = []
part2[len(part2)] = ""
for i in range(len(part2)):
    col = part2[i].strip()
    if col == "":
        sol2 += next(it)(current)
        current = []
        continue

    current.append(int(col))
print(f"Solution 2: {sol2}")
