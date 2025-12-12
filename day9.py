import sys
import math
import numpy as np

reds: list[tuple[int, int]] = []
while True:
    line = sys.stdin.readline().rstrip()

    if line == "":
        break

    x, y = line.split(",")

    reds.append((int(x), int(y)))

redss = np.array(reds)
large = np.array([reds for _ in reds])
large2 = large.transpose((1, 0, 2))
print(large.shape)
print(large2.shape)

areas = (np.abs(large - large2) + 1).prod(axis=-1)
print(areas)

index = int(np.argmax(areas))
a: int = index // len(reds)
b: int = index % len(reds)
sol1 = areas[a, b]
print(f"Solution 1: {sol1}")

raster = np.zeros((np.max(reds) + 1, np.max(reds) + 1), dtype=np.uint8)

x_prev, y_prev = reds[-1]
for x, y in reds:
    path = raster[
        min(x_prev, x) : max(x_prev, x) + 1, min(y_prev, y) : max(y_prev, y) + 1
    ]
    if x_prev == x:
        path[:, :] = np.where(path == 1, 1, 2)
    else:
        path[:, :] = np.where(path == 1, 1, 3)

    raster[x, y] = 1
    x_prev, y_prev = x, y

print(raster)

print(redss[:, 1])
indices_x = np.argsort(redss[:, 0])
indices_y = np.argsort(redss[:, 1])
mapping_x: dict[int, int] = {}
mapping_y: dict[int, int] = {}
inv_map_x: dict[int, int] = {}
inv_map_y: dict[int, int] = {}

for x, y in zip(indices_x, indices_y):
    if redss[x, 0] not in mapping_x:
        mapping_x[int(redss[x, 0])] = len(mapping_x)
        inv_map_x[len(mapping_x) - 1] = int(redss[x, 0])

    if redss[y, 1] not in mapping_y:
        mapping_y[int(redss[y, 1])] = len(mapping_y)
        inv_map_y[len(mapping_y) - 1] = int(redss[y, 1])

min_reds: list[tuple[int, int]] = []
for x, y in reds:
    min_reds.append((mapping_x[x], mapping_y[y]))

min_raster = np.zeros((len(mapping_x), len(mapping_y)), dtype=np.uint8)
x_prev, y_prev = min_reds[-1]
for x, y in min_reds:
    path = min_raster[
        min(x_prev, x) : max(x_prev, x) + 1, min(y_prev, y) : max(y_prev, y) + 1
    ]
    if x_prev == x:
        path[:, :] = np.where(path == 1, 1, 2)
    else:
        path[:, :] = np.where(path == 1, 1, 3)

    min_raster[x, y] = 1
    x_prev, y_prev = x, y

framed = np.zeros((min_raster.shape[0] + 2, min_raster.shape[1] + 2), dtype=np.uint8)
framed[1:-1, 1:-1] = min_raster

sys.setrecursionlimit(1000000)


def floodfill(arr, x, y):
    if x < 0 or x >= arr.shape[0]:
        return
    if y < 0 or y >= arr.shape[1]:
        return
    if arr[x, y] != 0:
        return
    arr[x, y] = 10
    floodfill(arr, x, y - 1)
    floodfill(arr, x - 1, y)
    floodfill(arr, x, y + 1)
    floodfill(arr, x + 1, y)


floodfill(framed, 0, 0)

print(min_raster.shape)
print(min_raster)
print(framed)

indices = np.argsort(areas.flatten())
flat_inverse = indices.flatten()[::-1]
index_i = np.remainder(flat_inverse, len(redss))
index_j = np.floor_divide(flat_inverse, len(redss))

print(areas[index_i, index_j])

for i, j in zip(index_i, index_j):
    point1 = min_reds[i]
    point2 = min_reds[j]
    # print(areas[i, j], point1, point2)
    x1, y1 = point1
    x2, y2 = point2
    orig1 = inv_map_x[x1], inv_map_y[y1]
    orig2 = inv_map_x[x2], inv_map_y[y2]
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)
    # print(" ", orig1, orig2)
    if np.all(framed[min_x + 1 : max_x + 2, min_y + 1 : max_y + 2] != 10):
        break

print(f"Solution 2: {areas[i, j]}")

exit(0)
