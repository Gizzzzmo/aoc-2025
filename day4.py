import sys
import numpy as np
from scipy.signal import convolve2d

paper: list[list[int]] = []
while True:
    line = sys.stdin.readline().rstrip()
    if line == "":
        break

    print(line)
    paper.append([1 if c == "@" else 0 for c in line])

filter = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
paper = np.array(paper)
print(paper)

total = 0
while True:
    grabbable = convolve2d(paper, filter, mode="same", boundary="fill", fillvalue=0) < 4
    grabbed = grabbable * paper

    paper -= grabbed

    n = grabbed.sum()
    print(n)
    total += n
    if n == 0:
        break

print(total)

# grabbable = (
#     convolve2d(positions, filter, mode="same", boundary="fill", fillvalue=0) >= 1
# )
# print(paper * grabbable)
