import sys

ranges: list[tuple[int, int]] = []
while True:
    line = sys.stdin.readline().rstrip()

    if line == "":
        break

    start, end = line.split("-")
    ranges.append((int(start), int(end)))

ings: list[int] = []

while True:
    line = sys.stdin.readline().rstrip()

    if line == "":
        break

    ings.append(int(line))

total = 0
for ing in ings:
    if any([b >= ing >= a for (a, b) in ranges]):
        total += 1
print(f"solution 1: {total}")

ranges.sort(key=lambda x: x[0])

total2 = 0
last = -1
for r in ranges:
    a, b = r
    if last >= a:
        a = last + 1

    if last < b:
        last = b
    if a > b:
        continue

    total2 += (b - a) + 1


print(f"solution 2: {total2}")
