import sys
import numpy as np

points: list[list[int]] = []

n_conn: int = int(sys.argv[1])

while True:
    line = sys.stdin.readline().rstrip()

    if line == "":
        break

    points.append([int(n) for n in line.split(",")])

pts1 = np.array([points for _ in points])
pts2 = pts1.transpose((1, 0, 2))

dists = np.sqrt(np.square(pts1 - pts2).sum(axis=-1)).flatten()
print(pts1.shape)
print(pts2.shape)
# print(dists)

clusters: dict[int, set[int]] = {i: set([i]) for i in range(len(points))}

indices = np.argsort(dists)
a = 0
b = 0
for index in indices[len(points) : n_conn * 2 + len(points) : 2]:
    a = index // len(points)
    b = index % len(points)
    if a in clusters[b]:
        continue
    for x in clusters[b]:
        if x != b:
            clusters[x].update(clusters[a])
    clusters[b].update(clusters[a])
    for x in clusters[a]:
        if x != a:
            clusters[x].update(clusters[b])
    clusters[a].update(clusters[b])

# print(clusters)
counts = np.zeros((len(points),), dtype=int)

for cluster in clusters.values():
    counts[len(cluster)] += 1

top3: list[int] = []
for i, count in enumerate(counts[::-1]):
    j = len(points) - i - 1
    for _ in range(count // j):
        top3.append(j)
        if len(top3) >= 3:
            break
    if len(top3) >= 3:
        break

print(top3)
sol1 = np.prod(top3)
print(f"Solution 1: {sol1}")

for index in indices[n_conn * 2 + len(points) :: 2]:
    if len(clusters[0]) == len(points):
        break
    a = index // len(points)
    b = index % len(points)

    if a in clusters[b]:
        continue
    for x in clusters[b]:
        if x != b:
            clusters[x].update(clusters[a])
    clusters[b].update(clusters[a])
    for x in clusters[a]:
        if x != a:
            clusters[x].update(clusters[b])
    clusters[a].update(clusters[b])


sol2 = points[a][0] * points[b][0]
print(f"Solution 2: {sol2}")

# print(indices)


# print(points)
