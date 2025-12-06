import math
import sys

ranges = sys.stdin.readline().split(",")

count = 0
sum = 0
orig = 0
count2 = 0
sum2 = 0
for r in ranges:
    low, high = r.split("-")
    print(f"{low}-{high}")
    i = int(low)
    print(f"diff: {int(high) - i}")
    while i <= int(high):
        string = str(i)
        for div in range(2, len(string) + 1):
            if len(string) % div != 0:
                continue
            if all(
                string[j * len(string) // div : (j + 1) * len(string) // div]
                == string[(j + 1) * len(string) // div : (j + 2) * len(string) // div]
                for j in range(div - 1)
            ):
                if div == 2:
                    sum += i
                sum2 += i
                count2 += 1
                print(f"  found: {i}")
                break

        if string[: len(string) // 2] == string[len(string) // 2 :]:
            count += 1
            orig += i
        i += 1

print(f"solution 1: {count} {sum} ({orig})")
print(f"solution 2: {count2} {sum2}")
